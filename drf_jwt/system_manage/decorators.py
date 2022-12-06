from django.shortcuts import redirect
from django.shortcuts import resolve_url
from django.core.exceptions import PermissionDenied
from system_manage.utils import getTokenUser
from rest_framework_simplejwt.state import token_backend

# 로그인 확인
def login_required(redirect_url='/login'):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            access_token = request.COOKIES.get("access_token", None)
            try:
                decoded_payload = token_backend.decode(access_token, verify=True)
            except:
                return redirect(resolve_url(redirect_url))                
            return function(request, *args, **kwargs)
        return wrapper
    return decorator


# 로그아웃 확인. 로그인시 -> 메인화면
def logout_required(redirect_url='/'):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            access_token = request.COOKIES.get("access_token", None)
            try:
                decoded_payload = token_backend.decode(access_token, verify=True)
                return redirect(resolve_url(redirect_url))
            except:
                pass   
            return function(request, *args, **kwargs)
        return wrapper
    return decorator


# 권한 체크
def permission_required(perm, redirect_url=None, raise_exception=False):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if isinstance(perm, str):
                perms = (perm,)
            else:
                perms = perm
            access_token = request.COOKIES.get("access_token", None)
            user = getTokenUser(token=access_token)
            if user.has_perms(perms):
                pass
            else:
                if raise_exception:
                    raise PermissionDenied
                else:
                    return redirect(resolve_url(redirect_url))
            return function(request, *args, **kwargs)
        return wrapper
    return decorator