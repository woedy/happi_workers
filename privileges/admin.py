from django.contrib import admin

from privileges.models import AdminPrivilege, PractitionerPrivilege, ClientPrivilege, HumanResourcesPrivilege, \
    AppointeePrivilege, AppointerPrivilege

# Register your models here.
admin.site.register(AdminPrivilege)
admin.site.register(PractitionerPrivilege)
admin.site.register(ClientPrivilege)
admin.site.register(HumanResourcesPrivilege)

admin.site.register(AppointeePrivilege)
admin.site.register(AppointerPrivilege)
