from rest_framework import status
from rest_framework.response import Response

def json_response(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)

        except ValidationError as e:
            return Response(
                data={
                    'data': None, 
                    'error': 404, 
                    'message': e.message,
                }, 
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={
                    'data': None, 
                    'error': 500, 
                    'message': e.message,
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
