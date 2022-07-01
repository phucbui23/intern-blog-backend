from rest_framework import status
from rest_framework.response import Response

def json_response(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            return Response(
                {
                    "data": data, 
                    "error": 0, 
                    "message": "success"
                }, 
                status=status.HTTP_200_OK
            )
            
        except ValueError as e:
            return Response(
                {
                    "data": None, 
                    "error": 500, 
                    "message": str(e)
                }, 
                status=status.HTTP_200_OK
            )            
    return wrapper
