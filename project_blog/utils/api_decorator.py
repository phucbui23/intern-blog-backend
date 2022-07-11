from django.core.paginator import Paginator
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from utils.constant import DEFAULT_ITEMS_PER_PAGE


def paginator(func):
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        _paginator = Paginator(
            object_list=data,
            per_page=DEFAULT_ITEMS_PER_PAGE,            
        )
        page = args[0].GET.get('page')
        page_objects = _paginator.get_page(page)

        return_data = {
            'objects': page_objects.object_list,
            'total_record': _paginator.count,
            'total_page': page_objects.paginator.num_pages,
            'current_page': page_objects.number,
        }
        return return_data
        
    return wrapper

def json_response(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)

        except ValidationError as e:
            return Response(
                data={
                    'data': None, 
                    'error': 404, 
                    'message': str(e),
                }, 
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={
                    'data': None, 
                    'error': 500, 
                    'message': str(e),
                }, 
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={
                    'data': data,
                    'error': 0,
                    'message': 'success'
                }, 
                status=status.HTTP_200_OK,
            )
            
    return wrapper
