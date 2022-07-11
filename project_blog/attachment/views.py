from datetime import datetime

from django.forms import ValidationError
from rest_framework.decorators import api_view
from user_account.models import User
# Create your views here.
from utils.api_decorator import json_response
from utils.messages import USER_NOT_FOUND

from .models import Attachment
from .serializers import AttachmentSerializer


@api_view(['POST'])
@json_response
def create_attachment(request):
    data = request.data.dict().copy()
    username = data.pop('user', None)
    file_name = data.pop('file_name', None) + str(datetime.now())
    
    try:
        user = User.objects.get(
            username=username,
        )
    except User.DoesNotExist:
        raise ValidationError(USER_NOT_FOUND)
        
    new_attachment = Attachment.objects.create(
        **data,
        user=user,   
        file_name=file_name, 
    )

    data = AttachmentSerializer(
        instance=new_attachment,
        many=False,
    ).data

    return data
        
# @api_view
# @json_response
# def get_attachment(request):
#     ...

# @api_view(['PUT'])
# @json_response
# def update_attachment(request):
#     ...
