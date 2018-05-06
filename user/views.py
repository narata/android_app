from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse, JsonResponse
from .models import Recommend, Photo, Business, Comment
from django.utils.timezone import now


# 注册
def create_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
    except Exception:
        result = False
    else:
        result = True
    return JsonResponse({
        "result": result
    })


# 登陆
def login(request):
    result = {}
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            result['result'] = True
            result['data'] = []
            result['data'].append({
                "userid": user.id,
                "username": username
            })
        else:
            result['result'] = False
            result['message'] = 'wrong user name or password'
    except MultiValueDictKeyError:
        result['message'] = 'parameter error'
    return JsonResponse(result)


# 注销
def logout(request):
    result = {}
    if request.user.is_authenticated():
        try:
            auth.logout(request)
            result['result'] = True
        except:
            result['result'] = False
    else:
        result['result'] = True
    return JsonResponse(result)


# 推荐
def get_user_business(request):
    result = {}
    try:
        user_id = int(request.GET['user_id'])
        result['result'] = True
        result['data'] = []
        recommend = Recommend.objects.filter(user_id=user_id)
        for data in recommend:
            photo = Photo.objects.filter(business=data.business)[0]
            result["data"].append({
                "business_id": data.business.id,
                "business_name": data.business.name,
                "img_url": photo.img_url
            })
    except Exception:
        result['result'] = False
    return JsonResponse(result)


# 获得餐厅详情
def get_business_detail(request):
    result = {}
    try:
        business_id = int(request.GET['business_id'])
        business = Business.objects.filter(id=int(business_id))
        photo = Photo.objects.filter(business=business[0])[0]
        result['result'] = True
        result['data'] = {
            "business_id": business[0].id,
            "business_name": business[0].name,
            "star": business[0].star,
            "attribute": business[0].attribute,
            "img_url": photo.img_url
        }
    except MultiValueDictKeyError:
        result['result'] = False
        result['message'] = 'parameter error'
    except Exception:
        result['result'] = False
    return JsonResponse(result)


# 评论
def add_comment(request):
    result = {}
    try:
        user_id = int(request.POST['user_id'])
        business_id = int(request.POST['business_id'])
        text = request.POST['text']
        star = float(request.POST['star'])
        comm = Comment(user_id=user_id, business_id=business_id, text=text, star=star, date=now())
        comm.save()
        result['result'] = True
    except MultiValueDictKeyError:
        result['result'] = False
        result['message'] = 'parameter error'
    # except Exception:
    #     result['result'] = False
    return JsonResponse(result)


# 吃过的
def eaten(request):
    result = {}
    try:
        user_id = int(request.GET['user_id'])
        comm = Comment.objects.filter(user_id=user_id).values('business_id', 'business__name').distinct()
        result['result'] = True
        result['data'] = []
        for buf in comm:
            result['data'].append({
                'business_id': buf['business_id'],
                'business_name': buf['business__name']
            })
    except MultiValueDictKeyError:
        result['result'] = False
        result['message'] = 'parameter error'
    except:
        result['result'] = False
    return JsonResponse(result)


# 查看自己评论
def get_self_comment(request):
    result = {}
    user_id = int(request.GET['user_id'])
    comm = Comment.objects.filter(user_id=user_id)
    result['result'] = True
    result['data'] = []
    for buf in comm:
        result['data'].append({
            "business_id": buf.business_id,
            "business_name": buf.business.name,
            "text": buf.text,
            "date": buf.date
        })
    return JsonResponse(result)


def test(request):
    return JsonResponse({1: 2})
