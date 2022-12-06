from django.urls import path, include
#APP
from rest_framework_simplejwt.views import TokenVerifyView
from api.views.authentication_views.auth_views import LoginView, ReissueTokenView, LogoutView

app_name='api'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), #토큰 검증 ..
    path('token/refresh/', ReissueTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_logoout'),
]