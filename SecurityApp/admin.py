from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Logon

# Register your models here.


class LogonInline(admin.StackedInline):
    model = Logon
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (LogonInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
