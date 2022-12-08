from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse
from system_manage.decorators import login_required, logout_required, permission_required
from system_manage.utils import getTokenUser
from django.utils.decorators import method_decorator


class HomeView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context['user'] = user

        return render(request, 'website_main.html', context)

class TestView(View):
    @method_decorator(login_required(redirect_url='system_manage:login'))
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context['user'] = user

        return render(request, 'website_test.html', context)