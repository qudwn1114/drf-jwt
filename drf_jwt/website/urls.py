from django.urls import path, include
from website.views.authentication_views.auth_views import HomeView


app_name='website'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]