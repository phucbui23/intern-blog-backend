from django.contrib import admin

from .models import Tag
from .models import BlogTag


admin.site.register(Tag)
admin.site.register(BlogTag)
