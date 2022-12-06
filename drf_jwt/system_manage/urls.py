from django.urls import path, include
from system_manage.views.system_manage_views.auth_views import HomeView

app_name='system_manage'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]