from django.contrib import admin

from keycloak.admin.realm import RealmAdmin
from keycloak.admin.server import ServerAdmin
from keycloak.models import Server, Realm

admin.site.register(Realm, RealmAdmin)
admin.site.register(Server, ServerAdmin)
