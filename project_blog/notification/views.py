from rest_framework.decorators import api_view

from utils.api_decorator import json_response

from .models import Notification
from .serializers import NotificationSerializer


# @api_view['POST']
# @json_response
# def create_notification(request):
#     return request.user
