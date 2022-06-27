from django.contrib import admin

# Register your models here.
from .models import UserDeviceToken
from .models import UserActivation
from .models import ResetPassWord


admin.site.register(UserDeviceToken)
admin.site.register(UserActivation)
admin.site.register( ResetPassWord )