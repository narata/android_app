# -*- coding: utf-8 -*-
# @Time     : 2018/4/26 9:49
# @Author   : Narata
# @Project  : android_app
# @File     : url.py
# @Software : PyCharm

from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^create_user$', views.create_user),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^get_user_business$', views.get_user_business),
    url(r'^get_business_detail$', views.get_business_detail),
    url(r'^add_comment$', views.add_comment),
    url(r'^eaten$', views.eaten),
    url(r'^get_self_comment$', views.get_self_comment),
    url(r'^test$', views.test),
    url(r'^search_business$', views.search_business),
    # url(r'^insert_user$', views.insert_user)
]