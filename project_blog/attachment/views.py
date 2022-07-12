from datetime import datetime

from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
# Create your views here.
from utils.api_decorator import json_response

from .models import Attachment
from .serializers import AttachmentSerializer


@api_view(['POST'])
@json_response
def create_attachment(request):
    data = request.POST.copy()
    user = request.user
    file = request.FILES.pop('file')[0]

    fs = FileSystemStorage(location='static/')
    fname = fs.save(file.name, file)
    # file_name = data.pop('file', '') + str(datetime.now())

    new_attachment = Attachment.objects.create(
        file_name=fname,
        display_name=file.name,
        file_path=fs.url(fname), 
        **data,
        user=user,   
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
