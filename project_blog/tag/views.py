from django.db.models import Count
from rest_framework.decorators import api_view

from utils.api_decorator import json_response

from .models import BlogTag


@api_view(['GET'])
@json_response
def get_most_used_tag(request):
    data = BlogTag.objects.values_list(
        'tag__name'
    ).annotate(
        tag_count=Count('tag')
    ).order_by(
        '-tag_count'
    )
    
    return data
