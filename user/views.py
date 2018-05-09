from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse, JsonResponse
from .models import Recommend, Photo, Business, Comment
from . import models
from django.utils.timezone import now
import uuid


# 注册
def create_user(request):
    try:
        username = request.POST['username']
        if 'password' in request.POST:
            password = request.POST['password']
        else:
            password = ''
        if 'email' in request.POST:
            email = request.POST['email']
        else:
            email = ''
        user1 = User.objects.create_user(username=username, email=email, password=password, first_name=username)
        user1.save()
        user2 = models.User(id=username, user_id=user1.id)
        user2.save()
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
                "username": username,
                "name": user.first_name
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
        user_id = request.GET['user_id']
        result['result'] = True
        result['data'] = []
        recommend = Recommend.objects.filter(user_id=user_id)
        for data in recommend:
            result["data"].append({
                "business_id": data.business.id,
                "business_name": data.business.name,
                "star": data.business.star,
                "attribute": data.business.attribute,
                "comment_count": data.business.comment_count,
                "value": data.value
            })
    except Exception:
        result['result'] = False
    return JsonResponse(result)


# 获得餐厅详情
def get_business_detail(request):
    result = {}
    try:
        business_id = request.GET['business_id']
        business = Business.objects.filter(id=business_id)
        photo = Photo.objects.filter(business=business[0])
        result['result'] = True
        result['data'] = {
            "business_id": business[0].id,
            "business_name": business[0].name,
            "star": business[0].star,
            "attribute": business[0].attribute,
            "comment_count": business[0].comment_count,
            "photo": [{
                'caption': buf.caption,
                'label': buf.label,
                'img_data': buf.img_data
            } for buf in photo]
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
        user_id = request.POST['user_id']
        business_id = request.POST['business_id']
        text = request.POST['text']
        star = float(request.POST['star'])
        comm = Comment(id=uuid.uuid1(), user_id=user_id, business_id=business_id, text=text, star=star, date=now())
        comm.save()
        user = comm.user
        user.average_stars = round((user.average_stars * user.comment_count + star) / (user.comment_count + 1), 2)
        user.comment_count += 1
        user.save()
        business = comm.business
        business.star = round((business.star * business.comment_count + star) / (business.comment_count + 1), 2)
        business.comment_count += 1
        business.save()
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
        user_id = request.GET['user_id']
        comm = Comment.objects.filter(user_id=user_id).values(
            'business__id', 'business__name', 'business__star', 'business__comment_count'
        ).distinct()
        result['result'] = True
        result['data'] = []
        for buf in comm:
            result['data'].append({
                'business_id': buf['business__id'],
                'business_name': buf['business__name'],
                'business_star': buf['business__star'],
                'business_comment_count': buf['business__comment_count']
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
    user_id = request.GET['user_id']
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


# 查找店铺
def search_business(request):
    result = {}
    business_name = request.GET['business_name']
    buss = Business.objects.filter(name__contains=business_name)
    result['result'] = True if len(buss) > 0 else False
    if len(buss) >= 20:
        buss = buss[:20]
    result['data'] = []
    for buf in buss:
        result['data'].append({
            'business_id': buf.id,
            'business_name': buf.name,
            'star': buf.star,
            'attribute': buf.attribute,
            'comment_count': buf.comment_count
        })
    return JsonResponse(result)


# # 导入user
# def insert_user(request):
#     import json
#     from . import models
#     with open('databases/dataset/user.json', 'rb') as fp:
#         i = 0
#         for data in fp.readlines():
#             i += 1
#             json_data = json.loads(data)
#             user1 = User.objects.create_user(
#                 username=json_data['user_id'],
#                 password='password',
#                 first_name=json_data['name'],
#                 last_name=json_data['name']
#             )
#             user1.save()
#             user2 = models.User(
#                 id=json_data['user_id'],
#                 average_stars=json_data['average_stars'],
#                 comment_count=json_data['review_count'],
#                 user_id=user1.id
#             )
#             user2.save()
#             print(i)
#     return JsonResponse({'result': True})


def test(request):
    return JsonResponse({1: 2})
