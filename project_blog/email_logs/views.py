from django.shortcuts import render
from requests import request
from rest_framework.decorators import api_view
from email_logs.models import EmailLogs
from email_logs.serializers import EmailLogsSerialier
from utils.api_decorator import json_response
# Create your views here.
