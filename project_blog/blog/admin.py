from django.contrib import admin

from .models import Blog, BlogHistory, BlogLike


admin.site.register(Blog)
admin.site.register(BlogHistory)
admin.site.register(BlogLike)
