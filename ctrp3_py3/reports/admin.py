from django.contrib import admin

from .models import Department, DepartmentToOrgCrosswalk, StopRecord

admin.site.register(Department)
admin.site.register(DepartmentToOrgCrosswalk)
admin.site.register(StopRecord)
