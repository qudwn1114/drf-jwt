from django.urls import path, include
#APP
from rest_framework_simplejwt.views import TokenVerifyView
from api.views.authentication_views.auth_views import LoginView, ReissueTokenView, LogoutView

from api.views.test_views.test_views import TestView

app_name='api'
urlpatterns = [
    path('login/', LoginView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()), #토큰 검증 ..
    path('token/refresh/', ReissueTokenView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('test/', TestView.as_view()),
]