from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import User , EmployeeProfile , Department , Level


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Required Info', {'fields': ('role','employee_profile')}),  
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Required Info', {'fields': ('first_name','last_name','email','role','employee_profile')}),
    )
    def save_model(self, request, obj, form, change):
        new_user =False 
        if obj.pk == None:
            new_user = True 
        super().save_model(request, obj, form, change)
        if new_user:
            # send email 
            pass 
@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('id','department','level','manager')

admin.site.register(Department)
admin.site.register(Level)
