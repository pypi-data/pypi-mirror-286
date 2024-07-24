from django_keycloak_lma.base.aio.mixins import WellKnownMixin
from django_keycloak_lma.base.openid_connect import (
    KeycloakOpenidConnect as SyncKeycloakOpenidConnect,
    PATH_WELL_KNOWN,
)

__all__ = (
    'KeycloakOpenidConnect',
)


class KeycloakOpenidConnect(WellKnownMixin, SyncKeycloakOpenidConnect):
    def get_path_well_known(self):
        return PATH_WELL_KNOWN
