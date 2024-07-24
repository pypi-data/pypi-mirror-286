from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework.views import exception_handler, set_rollback
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.exceptions import APIException


class BaseErrorResponse(APIException):
    """
        {
            'status': Duplicate HTTP status code
            'detail': Description of the error that occurred (or null)
            'validation_errors': List of parameters and description of errors encountered during validation of request parameters (or null)
            'code': Error code. It is needed to instruct the client to perform some action when an error occurs (or null)
            'payload_data': It contains useful information for troubleshooting
        }
    """

    def __init__(self, detail=None, validation_errors=None, code=None, payload_data=None):
        self.detail = {
            'status': self.status_code,
            'detail': detail,
            'validation_errors': validation_errors,
            'code': code,
            'payload_data': payload_data
        }


class Conflict(BaseErrorResponse):
    status_code = status.HTTP_409_CONFLICT


class Validate(BaseErrorResponse):
    status_code = status.HTTP_400_BAD_REQUEST


class PermissionDenied(BaseErrorResponse):
    status_code = status.HTTP_403_FORBIDDEN


class NotFound(BaseErrorResponse):
    status_code = status.HTTP_404_NOT_FOUND


class AuthenticationFailed(BaseErrorResponse):
    status_code = status.HTTP_401_UNAUTHORIZED


class BadGateway(BaseErrorResponse):
    status_code = status.HTTP_502_BAD_GATEWAY


class RequestTimeout(BaseErrorResponse):
    status_code = status.HTTP_408_REQUEST_TIMEOUT


class KeycloakOpenIdProfileNotFound(NotFound):
    pass


class TokensExpired(AuthenticationFailed):
    pass


def custom_exception_handler(exc, context):
    """Custom error handler"""

    if isinstance(exc, BaseErrorResponse):
        return exception_handler(exc, context)
    else:

        if isinstance(exc, Http404):
            exc = exceptions.NotFound()
        elif isinstance(exc, PermissionDenied):
            exc = exceptions.PermissionDenied()

        if isinstance(exc, exceptions.APIException):
            headers = {}
            if getattr(exc, 'auth_header', None):
                headers['WWW-Authenticate'] = exc.auth_header
            if getattr(exc, 'wait', None):
                headers['Retry-After'] = '%d' % exc.wait

            data = dict()

            data['status'] = exc.status_code
            data['code'] = None
            data['detail'] = None
            data['payload_data'] = None
            data['validation_errors'] = None

            if exc.status_code == 400:
                data['validation_errors'] = exc.detail
            else:
                if isinstance(exc.detail, str):
                    data['detail'] = exc.detail
                else:
                    data['payload_data'] = exc.detail

            set_rollback()
            return Response(data, status=exc.status_code, headers=headers)

        return None


