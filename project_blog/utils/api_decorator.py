from rest_framework.response import Response
from rest_framework import status
def json_response(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args,  **kwargs)       
        except Exception as e:
            return Response(data={'data': None, 'error_code': 500, 'message': str(e)}, status=status.HTTP_200_OK)
        else:
            return Response(data={'data': data, 'error_code':0, 'message': 'success'})
    return wrapper
