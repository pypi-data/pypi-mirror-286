import logging
from typing import Set
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from jose.exceptions import (
    ExpiredSignatureError,
    JWTClaimsError,
    JWTError,
)
from keycloak.base.exceptions import KeycloakClientError
from rest_framework.authentication import BasicAuthentication
from rest_framework import HTTP_HEADER_ENCODING
import keycloak.services.oidc_profile
import keycloak.services.messages as messages
from keycloak.services import exceptions

AUTH_HEADER_TYPES = ('Bearer',)

if not isinstance(AUTH_HEADER_TYPES, (list, tuple)):
    AUTH_HEADER_TYPES = (AUTH_HEADER_TYPES,)

AUTH_HEADER_TYPE_BYTES: Set[bytes] = {
    h.encode(HTTP_HEADER_ENCODING) for h in AUTH_HEADER_TYPES
}

logger = logging.getLogger(__name__)


class KeycloakPasswordAuthentication(BasicAuthentication):
    def auth(self, request, username, password, user):

        if not hasattr(request, 'realm'):
            raise ImproperlyConfigured(
                'Add BaseKeycloakMiddleware to middlewares')

        if not request.realm:
            # If request.realm does exist, but it is filled with None, we
            # can't authenticate using Keycloak
            return None, None

        try:
            keycloak_openid_profile = keycloak.services \
                .oidc_profile.update_or_create_from_password_credentials(
                client=request.realm.client,
                username=username,
                password=password,
                user=user
            )
        except KeycloakClientError as api_ex:
            payload_text = None
            try:
                payload_text = api_ex.original_exc.response.text
            except Exception as ex:
                pass
            message = messages.get_backend_message('KeycloakPasswordAuthentication',
                                                   messages.get_message(messages.FAIL_AUTHENTICATION_ERROR))
            logger.debug(message)
            raise exceptions.AuthenticationFailed(detail=message, payload_data=payload_text)
        else:
            return keycloak_openid_profile.user, keycloak_openid_profile

    def authenticate_credentials(self, userid, password, request=None):
        # Base auth:
        UserModel = get_user_model()

        try:
            user = UserModel._default_manager.get_by_natural_key(userid)
        except UserModel.DoesNotExist:
            message = messages.get_backend_message('KeycloakPasswordAuthentication',
                                                   messages.get_message(messages.FAIL_AUTHENTICATION_ERROR))
            logger.debug(message)
            raise exceptions.AuthenticationFailed(detail=message)
        # keycloak-auth:
        user, oidc_profile = self.auth(request, userid, password, user)
        if user is None:
            message = messages.get_backend_message('KeycloakPasswordAuthentication',
                                                   messages.get_message(messages.FAIL_AUTHENTICATION_ERROR))
            logger.debug(message)
            raise exceptions.AuthenticationFailed(detail=message)

        return user, oidc_profile


class KeycloakTokenAuthentication(KeycloakAuthorizationBase):
    www_authenticate_realm = "api"
    media_type = "application/json"
    header_key = "HTTP_AUTHORIZATION"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate(self, request):

        if not hasattr(request, 'realm'):
            raise ImproperlyConfigured('Add BaseKeycloakMiddleware to middlewares')

        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        oidc_profile = self.get_profile(request, raw_token)

        return oidc_profile.user, oidc_profile

    def authenticate_header(self, request):
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header = request.META.get(self.header_key)

        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise exceptions.AuthenticationFailed(detail='Authorization header must contain two space-delimited values')

        return parts[1]

    def get_profile(self, request, access_token):
        try:
            oidc_profile = keycloak.services.oidc_profile.get_from_id_token(
                client=request.realm.client, id_token=access_token, check_client=True)
            initiate_time = timezone.now()
            if oidc_profile.expires_before is None or initiate_time > oidc_profile.expires_before:
                raise ExpiredSignatureError()
        except ExpiredSignatureError:
            # If the signature has expired.
            message = messages.get_backend_message('KeycloakTokenAuthentication', messages.get_message(messages.EXPIRED_SIGNATURE_ERROR))
            logger.debug(message)
            raise exceptions.AuthenticationFailed(detail=message)
        except JWTClaimsError as ex:
            message = messages.get_backend_message_with_error('KeycloakTokenAuthentication', messages.get_message(messages.JWT_CLAIMS_ERROR),
                                                              str(ex))
            logger.debug(message)
            raise exceptions.AuthenticationFailed(detail=message)
        except JWTError:
            # The signature is invalid in any way.
            message = messages.get_backend_message('KeycloakTokenAuthentication', messages.get_message(messages.JWT_ERROR))
            logger.debug(message)
            raise exceptions.AuthenticationFailed(detail=message)

        return oidc_profile
