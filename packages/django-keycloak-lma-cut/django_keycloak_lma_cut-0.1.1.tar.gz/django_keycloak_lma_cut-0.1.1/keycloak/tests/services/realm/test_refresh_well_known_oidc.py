import mock

from django.test import TestCase

from keycloak.factories import RealmFactory
from keycloak.tests.mixins import MockTestCaseMixin

import keycloak.services.realm


class ServicesRealmRefreshWellKnownOIDCTestCase(
        MockTestCaseMixin, TestCase):

    def setUp(self):
        self.realm = RealmFactory(
            name='test-realm',
            _well_known_oidc='empty'
        )

        keycloak_oidc_mock = mock.MagicMock()
        keycloak_oidc_mock.well_known.contents = {'key': 'value'}
        self.setup_mock('keycloak.base.realm.KeycloakRealm.open_id_connect',
                        return_value=keycloak_oidc_mock)

    def test_refresh_well_known_oidc(self):
        """
        Case: An update is requested for the .well-known for a specified realm.
        Expected: The .well-known is updated.
        """
        self.assertEqual(self.realm._well_known_oidc, 'empty')

        keycloak.services.realm.refresh_well_known_oidc(
            realm=self.realm
        )

        self.assertEqual(self.realm._well_known_oidc, '{"key": "value"}')
