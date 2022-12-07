from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpRequest, QueryDict, JsonResponse
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from system_manage.models import AccessPermission
from system_manage.views.system_manage_views.permission_manage_views import get_access_perms
from system_manage.utils import getTokenUser
from django.utils.decorators import method_decorator
from system_manage.decorators import login_required, logout_required, permission_required


class AccessManageView(View):
    """
    그룹 권한 관리 화면
    김병주/2022.12.07
    """
    @method_decorator(login_required(redirect_url='system_manage:login'))
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context['user'] = user

        groups = Group.objects.all()
        context['groups'] = groups

        group_id = request.GET.get('group_id', None)
        if group_id:
            context['selected_group'] = Group.objects.get(pk=group_id)

            paginate_by = '10'
            page = request.GET.get('page', '1')
            filter_dict = {}
            search_type = request.GET.get('search_type', '')
            search_keyword = request.GET.get('search_keyword', '')

            if search_keyword:
                context['search_type'] = search_type
                context['search_keyword'] = search_keyword
                filter_dict[search_type + '__icontains'] = search_keyword
                qset = AccessPermission.objects.filter(**filter_dict).order_by('id')
            else:
                qset = AccessPermission.objects.all().order_by('id')

            for perm in qset:
                perm.hasPerm = check_group_permission(group_id, perm.id)
                
            paginator = Paginator(qset, paginate_by)
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page = 1
                page_obj = paginator.page(page)
            except EmptyPage:
                page = 1
                page_obj = paginator.page(page)
            except InvalidPage:
                page = 1
                page_obj = paginator.page(page)
            pagelist = paginator.get_elided_page_range(page, on_each_side=3, on_ends=1)
            context['pagelist'] = pagelist
            context['page_obj'] = page_obj

        return render(request, 'system_manage/access_manage.html', context)

    @method_decorator(login_required(redirect_url='system_manage:login'))
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        선택된 그룹의 권한 설정을 변경합니다.
        """
        try:
            group_id = request.POST['group_id']
            permission_id = request.POST['permission_id']
            has_perm = str(request.POST['has_perm']).lower() == 'true'

            selected_group = get_group(group_id)
            if not selected_group:
                raise Exception('유효하지 않은 그룹입니다.')

            set_group_permission(group_id, permission_id, has_perm)
            
            # Get all access permissions and check its possession.
            perms = get_access_perms()
            for perm in perms:
                perm.hasPerm = check_group_permission(group_id, perm.id)

        except Exception as e:
            return JsonResponse({"message": e.args[0]}, status = 400)
        
        return JsonResponse({'message' : '변경 완료'}, status = 201)



class GroupManageView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        그룹 생성
        """
        try:
            group_name = request.POST['group_name']
            is_valid = check_group_name(group_name)
            if not is_valid:
                raise Exception('생성 불가능한 그룹 이름입니다.')
            create_group(group_name)
        except Exception as e:
            print(e)
            return JsonResponse({"message": e.args[0]}, status = 400)
        return JsonResponse({'message' : '생성 완료'}, status = 201)

    def delete(self, request: HttpRequest, *args, **kwargs):
        """
        그룹 삭제
        """
        try:
            request.DELETE = QueryDict(request.body)
            group_id = request.DELETE['group_id']
            can_be_deleted = check_group_deletion(group_id)
            if not can_be_deleted:
                raise Exception('해당 그룹에 사용자가 있어 삭제가 불가능합니다.')

            is_deleted = delete_group(group_id)
            if not is_deleted:
                raise Exception('그룹을 삭제하는 중에 오류가 발생했습니다.')
        except Exception as e:
            return JsonResponse({"message": e.args[0]}, status = 400)

        return JsonResponse({'message' : '그룹 삭제완료.'}, status = 200)


def check_group_name(group_name):
    """
    그룹이름의 중복 여부를 체크합니다.
    """
    grp_qset = Group.objects.filter(
        name=group_name
    )
    return not grp_qset.exists()

def create_group(group_name):
    """
    그룹을 생성합니다.
    """
    created = Group.objects.create(
        name=group_name
    )
    return created

def check_group_deletion(gid):
    return not User.objects.filter(
        **{
            'groups__id': gid
        }
    ).exists()

def delete_group(gid):
    _, res_dict = Group.objects.filter(id=gid).delete()
    return res_dict[Group._meta.label] == 1

def get_group(gid):
    grp_qset = Group.objects.filter(id=gid)
    
    grp = None
    if grp_qset.exists():
        grp = grp_qset.first()
        
    return grp 


def set_group_permission(group_id, permission_id, has_perm):
    """
    그룹의 권한 소유여부를 변경합니다.
    """

    # TODO: 개별 함수로 분리하여 예외처리할 것.
    perm = AccessPermission.objects.get(id=permission_id)

    group = get_group(group_id)

    if (has_perm):
        group.permissions.add(perm)
    else:
        group.permissions.remove(perm)

def check_group_permission(group_id, permission_id):
    """
    그룹의 권한 소유여부를 체크합니다.
    """

    return Group.objects.filter(id=group_id, **{
        'permissions__id': permission_id
    }).exists()

