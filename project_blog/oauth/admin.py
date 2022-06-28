from django.contrib import admin

# Register your models here.

from .models import ResetPassword, UserActivation, UserDeviceToken

admin.site.register(UserDeviceToken)
admin.site.register(UserActivation)
admin.site.register(ResetPassword)
