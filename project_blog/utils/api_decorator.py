def json_response(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            return Response({data: data, ...}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({data: None, error: 500, message: "Internal Server Error"}, status=status.HTTP_200_OK)
    return wrapper
