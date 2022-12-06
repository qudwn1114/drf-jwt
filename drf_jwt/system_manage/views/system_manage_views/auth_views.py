from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views.generic import View
from django.http import HttpRequest
from django.contrib.auth.models import Group, User
from system_manage.utils import getTokenUser


# Create your views here.
class HomeView(View):
    '''
    관리자 메인 화면
    김병주/2022.12.06
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context['user'] = user

        return render(request, 'system_manage/admin_main.html', context)