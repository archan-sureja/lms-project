from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import User , EmployeeProfile , Department , Level

class EmployeeProfileInline(admin.TabularInline):
    model =  EmployeeProfile 
    extra = 1 

@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role',)}),  
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role',)}),
    )
    inlines = [EmployeeProfileInline]

admin.site.register(Department)
admin.site.register(Level)