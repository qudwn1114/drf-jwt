from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse
from system_manage.decorators import login_required, logout_required, permission_required
from system_manage.utils import getTokenUser
from django.utils.decorators import method_decorator


class HomeView(View):
    @method_decorator(login_required(redirect_url='/login'))
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context['user'] = user

        return render(request, 'home.html', context)


class LoginView(View):
    @method_decorator(logout_required(redirect_url='/'))
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context['user'] = user

        return render(request, 'login.html', context)