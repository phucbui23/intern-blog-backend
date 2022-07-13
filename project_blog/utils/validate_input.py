import re
from rest_framework.exceptions import ValidationError
from .messages import *

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

def validate_email(email):
    if (not email):
        raise ValidationError(EMPTY_EMAIL_FIELDS)
    
    if (len(email) > 255):
        raise ValidationError(MAX_LENGTH_EMAIL)

    if (not re.match(EMAIL_REGEX, email)):
        raise ValidationError(INVALID_EMAIL)
    

def validate_password(password):
    if (not password):
        raise ValidationError(EMPTY_PASSWORD_FIELDS)
    
    if (len(password) > 255 or len(password) < 8):
        raise ValidationError(INVALID_LENGTH_PASSWORD)

    if (password.isdigit()):
        raise ValidationError(INVALID_PASSWORD)


def validate_fullname(full_name):
    if (not full_name):
        raise ValidationError(EMPTY_FULLNAME_FIELDS)
    
    if (len(full_name) > 255):
        raise ValidationError(MAX_LENGTH_FULLNAME)


def validate_nickname(nick_name):
    if (not nick_name):
        raise ValidationError(EMPTY_NICKNAME_FIELDS)
    
    if (len(nick_name) > 255):
        raise ValidationError(MAX_LENGTH_NICK_NAME)


def validate_phone_number(phone_number):
    if (not phone_number):
        raise ValidationError(EMPTY_PHONENUMBER_FIELDS)

    if (len(phone_number) > 16):
        raise ValidationError(MAX_LENGTH_PHONE_NUMBER)
    