# from rest_framework import authentication
# import jwt

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView

# class JWTAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         return super().authenticate(request)
