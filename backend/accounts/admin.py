from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import User , EmployeeProfile , Department , Level


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role','employee_profile')}),  
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role','employee_profile')}),
    )

admin.site.register(Department)
admin.site.register(Level)
admin.site.register(EmployeeProfile)