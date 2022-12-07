from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views.generic import View
from django.http import HttpRequest
from django.contrib.auth.models import Group, User
from system_manage.utils import getTokenUser
from django.utils.decorators import method_decorator
from system_manage.decorators import login_required, logout_required, permission_required


# Create your views here.
class HomeView(View):
    '''
    관리자 메인 화면
    김병주/2022.12.06
    '''
    @method_decorator(login_required(redirect_url='system_manage:login'))
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context['user'] = user

        return render(request, 'system_manage/admin_main.html', context)

class LoginView(View):
    '''
    관리자 로그인 기능
    김병주/2022.12.06
    '''
    @method_decorator(logout_required(redirect_url='system_manage:home'))
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}

        return render(request, 'system_manage/admin_login.html', context)