"""
from keycloak.auth.permissions import UserPermission
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, parser_classes, authentication_classes, \
    permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import logout as django_logout

from keycloak import serializers as keycloak_serializers
from keycloak.auth.backends import KeycloakPasswordAuthentication, KeycloakTokenAuthentication
from keycloak.services import oidc_profile, remote_client

from . import serializers
from .choices import UserGroup


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
@authentication_classes([KeycloakPasswordAuthentication])
def login(request):
    if not hasattr(request, 'auth'):
        raise Exception("Section 'auth' was not found")

    auth_data = keycloak_serializers.TokenSerializer(request.auth).data

    return Response(auth_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
@authentication_classes([KeycloakTokenAuthentication])
@permission_classes((UserPermission(UserGroup.EXCHANGE),))
def check_access(request):

    return Response(status=status.HTTP_200_OK)
"""
