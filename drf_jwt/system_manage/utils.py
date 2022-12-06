from django.contrib.auth.models import User
from rest_framework_simplejwt.state import token_backend


def getTokenUser(token:str) -> object:
    '''
        jwt token 으로 부터 User 반환
    '''
    try:
        decoded_payload = token_backend.decode(token, verify=True)
        user_uid=decoded_payload['user_id']
        user = User.objects.get(pk=user_uid)
    except:
        user = None
        
    return user

    
