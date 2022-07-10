from django.contrib import admin

# Register your models here.
from .models import EmailLogs


admin.site.register(EmailLogs)
