from django.contrib import admin

# Register your models here.
from .models import Blog
from .models import BlogHistory
from .models import BlogLike


admin.site.register(Blog)
admin.site.register(BlogHistory)
admin.site.register(BlogLike)
