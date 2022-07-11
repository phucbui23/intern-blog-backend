from datetime import datetime
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError
from utils.messages import INVALID_TOKEN, EXPIRED_TOKEN, PLEASE_LOGIN
from .models import UserDeviceToken

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_headers = request.headers.get('Authorization')

        if auth_headers is None:
            return None

        auth = auth_headers.split()
        
        if ((len(auth) == 1) or (len(auth) > 2)):
            raise AuthenticationFailed('Invalid Authorization Header')

        if auth[0] not in settings.SIMPLE_JWT['AUTH_HEADER_TYPES']:
            raise AuthenticationFailed('Invalid Auth Header Type')
        
        try:
            token = UserDeviceToken.objects.get(token=auth[1])
        except UserDeviceToken.DoesNotExist:
            raise NotFound(INVALID_TOKEN)
        
        if not token.active:
            raise AuthenticationFailed(PLEASE_LOGIN)

        expr = token.created_at + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        
        if expr < datetime.now():
            token.active = False
            token.deactived_At = datetime.now()
            token.save()
            raise ValidationError(EXPIRED_TOKEN)

        return (token.author, auth[1])
