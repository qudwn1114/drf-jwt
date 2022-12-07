from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models.query import QuerySet
from django.http import HttpRequest, QueryDict, JsonResponse
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.db import transaction, IntegrityError
from system_manage.models import AccessPermission
from system_manage.utils import getTokenUser
from django.utils.decorators import method_decorator
from system_manage.decorators import login_required, logout_required, permission_required


class AccessPermissionManageView(View):
    """
    접근 권한 관리 화면
    김병주/2022.12.08
    """
    @method_decorator(login_required(redirect_url='system_manage:login'))
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context['user'] = user

        paginate_by = '10'
        page = request.GET.get('page', '1')
        filter_dict = {}
        search_type = request.GET.get('search_type', '')
        search_keyword = request.GET.get('search_keyword', '')

        if search_keyword:
            context['search_type'] = search_type
            context['search_keyword'] = search_keyword
            filter_dict[search_type + '__icontains'] = search_keyword
            qset = AccessPermission.objects.filter(**filter_dict).order_by('-id')
        else:
            qset = AccessPermission.objects.all().order_by('-id')

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

        return render(request, 'system_manage/permission_manage.html', context)

    @method_decorator(login_required(redirect_url='system_manage:login'))
    def post(self, request: HttpRequest, *args, **kwargs):
        """
        권한을 생성힙니다.
        """
        try:
            with transaction.atomic():
                perm_name = request.POST.get('name', None)
                perm_url = request.POST.get('codename', None)

                # Create access(read or write) permission.
                _, is_read_created = get_or_create_read_perm(perm_name, perm_url)
                _, is_write_created = get_or_create_write_perm(perm_name, perm_url)
                if not (is_read_created or is_write_created):
                    raise Exception('이미 존재하는 메뉴 입니다.')
        except IntegrityError:
            return JsonResponse({"message": '이미 존재하는 메뉴 입니다.'}, status = 400)
        except Exception as e:
            print(e.args[0])
            return JsonResponse({"message": e.args[0]}, status = 400)

        return JsonResponse({'message' : '생성 완료'}, status = 201)

    @method_decorator(login_required(redirect_url='system_manage:login'))
    def put(self, request: HttpRequest, *args, **kwargs):
        """
        권한을 수정힙니다.
        """
        try:
            request.PUT = QueryDict(request.body)
            perm_id = request.PUT.get('id', None)
            perm_name = request.PUT.get('name', None)
            perm_url = request.PUT.get('codename', None)
            
            # Update access permission.
            is_updated = update_access_perm(perm_id, perm_name, perm_url)
            if not is_updated:
                raise Exception('해당 값으로 수정할 수 없습니다.')

        except Exception as e:
            return JsonResponse({"message": e.args[0]}, status = 400)

        return JsonResponse({'message' : '수정 완료'}, status = 201)

    @method_decorator(login_required(redirect_url='system_manage:login'))
    def delete(self, request: HttpRequest, *args, **kwargs):
        """
        권한을 삭제힙니다.
        """
        try:
            request.DELETE = QueryDict(request.body)
            perm_id = request.DELETE.get('id', None)
            
            # Delete access permission.
            is_deleted = delete_access_perm(perm_id)
            if not is_deleted:
                raise Exception('삭제 불가능한 항목입니다.')

        except Exception as e:
            return JsonResponse({"message": e.args[0]}, status = 400)

        return JsonResponse({'message' : '삭제 완료'}, status = 201)

def get_or_create_read_perm(name, perm_url):
    perm_url = normalize_url(perm_url)
    
    return AccessPermission.objects.get_or_create(
        name=name,
        codename=make_codename(perm_url),
        content_type=AccessPermission.PERMISSION_TYPE.READ,
    )

def get_or_create_write_perm(name, perm_url):
    perm_url = normalize_url(perm_url)

    return AccessPermission.objects.get_or_create(
        name=name,
        codename=make_codename(perm_url),
        content_type=AccessPermission.PERMISSION_TYPE.WRITE,
    )

def update_access_perm(id, name, perm_url):
    updated_rows = AccessPermission.objects.filter(id=id).update(
        name=name,
        codename=make_codename(perm_url)
    )

    return updated_rows == 1

def delete_access_perm(id):
    _, res_dict = AccessPermission.objects.filter(id=id).delete()
    return res_dict[AccessPermission._meta.label] == 1


def normalize_url(perm_url: str):
    # if not perm_url.startswith('/'):
    #     perm_url = '/' + perm_url
    return perm_url.lower()

def make_codename(perm_url: str):
    perm_url = normalize_url(perm_url)

    return str(perm_url)\
        # .replace('-', '_')\
        # .replace('/', '_')\
        # .replace('_', '', 1)

def get_access_perms():
    qset = AccessPermission.objects.all()
    return filter_access_perms(qset)

def filter_access_perms(qset: QuerySet):
    for perm in qset:
        # Convert codename to url.
        perm.codename = normalize_url(perm.codename)

        # Convert content type.
        if perm.content_type_id == AccessPermission.PERMISSION_TYPE.READ.id:
            perm.content_type_id = "Read"
        elif perm.content_type_id == AccessPermission.PERMISSION_TYPE.WRITE.id:
            perm.content_type_id = "Write"

    return qset 