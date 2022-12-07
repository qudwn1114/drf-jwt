from django.urls import path, include
from system_manage.views.system_manage_views.auth_views import HomeView, LoginView
from system_manage.views.system_manage_views.access_manage_views import AccessManageView, GroupManageView
from system_manage.views.system_manage_views.permission_manage_views import AccessPermissionManageView

app_name='system_manage'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    # 권한 접근 관리

    path('access-manage/', AccessManageView.as_view(), name='access_manage'),
    path('group-manage/', GroupManageView.as_view(), name='group_manage'),
    path('permission-manage/', AccessPermissionManageView.as_view(), name='permission_manage'),

]