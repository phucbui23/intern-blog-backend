from datetime import datetime
from django.conf import settings
from rest_framework.exceptions import NotFound,ValidationError
from utils.messages import INVALID_TOKEN,EXPIRED_TOKEN,PLEASE_LOGIN

from oauth.models import UserDeviceToken

def validate_token(token):
    try:
        token = UserDeviceToken.objects.get(token=token)
    except UserDeviceToken.DoesNotExist:
        raise NotFound(INVALID_TOKEN)
        
    if not token.active:
        raise Exception(PLEASE_LOGIN)
    
    expr = token.created_at + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

    if expr < datetime.now():
        token.active = False
        token.deactived_at = datetime.now()
        token.save()
        raise ValidationError(EXPIRED_TOKEN)
    
    return token
