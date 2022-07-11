from django.utils.crypto import get_random_string
def gen_token():
    return get_random_string(length=30)
    