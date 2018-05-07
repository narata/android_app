from django.db import models
import django.contrib.auth.models
from django.utils.timezone import now


class Business(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    star = models.FloatField()
    attribute = models.CharField(max_length=200)
    comment_count = models.IntegerField(default=0)
    

class Photo(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    business = models.ForeignKey(Business)
    img_data = models.TextField(default=None)
    caption = models.CharField(max_length=200, default=None)
    label = models.CharField(max_length=200, default=None)
    
    
# class User(models.Model):
#     id = models.CharField(max_length=50, primary_key=True)
#     name = models.CharField(max_length=50)
#     comment_count = models.IntegerField()
#     average_stars = models.FloatField()
#     user = models.ForeignKey(django.contrib.auth.models.User, default=None)


class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    comment_count = models.IntegerField(default=0)
    average_stars = models.FloatField(default=0)
    user = models.ForeignKey(django.contrib.auth.models.User)


class Comment(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    business = models.ForeignKey(Business, default=None)
    user = models.ForeignKey(User, default=None)
    date = models.DateTimeField()
    text = models.TextField()
    star = models.FloatField()
    
    
class Recommend(models.Model):
    business = models.ForeignKey(Business, default=None)
    user = models.ForeignKey(User, default=None)
