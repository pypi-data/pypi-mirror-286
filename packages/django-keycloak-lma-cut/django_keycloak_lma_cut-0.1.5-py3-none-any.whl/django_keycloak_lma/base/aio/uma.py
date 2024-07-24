from django_keycloak_lma.base.aio.mixins import WellKnownMixin
from django_keycloak_lma.base.uma import KeycloakUMA as SyncKeycloakUMA, PATH_WELL_KNOWN

__all__ = (
    'KeycloakUMA',
)


class KeycloakUMA(WellKnownMixin, SyncKeycloakUMA):
    def get_path_well_known(self):
        return PATH_WELL_KNOWN
