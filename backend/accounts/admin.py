from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import User , EmployeeProfile , Department , Level
from .tasks import send_credentials_email_task

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
        if obj.pk is None:
            new_user = True 
        super().save_model(request, obj, form, change)
        if new_user:
            raw_password  = form.cleaned_data.get('password1')
            print("sending email with this data ->",obj.email, obj.username, raw_password, obj.get_role_display())
            send_credentials_email_task.delay(obj.email, obj.username, raw_password, obj.get_role_display())
    
@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('id','department','level','manager')

admin.site.register(Department)
admin.site.register(Level)
