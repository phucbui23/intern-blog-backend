from django.core.paginator import Paginator
from api_decorator import json_response

ORPHANS_THRESHHOLD = 2
DEFAULT_ITEMS_PER_PAGE = 5

def listing_api(request, obj):
    page_number = request.GET.get("page", 1)
    items_per_page = request.GET.get("per_page", DEFAULT_ITEMS_PER_PAGE)

    paginator = Paginator(
        object_list=obj, 
        per_page=items_per_page,
        orphans=ORPHANS_THRESHHOLD,
        allow_empty_first_page=False # check empty obj_list
    )
    page_obj = paginator.get_page(page_number)
    page_data = [data for data in page_obj.obj]

    payload = {
        'page': {
            'current': page_obj.number,
            'has_next': page_obj.has_next,
            'has_prev': page_obj.has_previous,
        },
        'data': page_data,
    }

    return payload
