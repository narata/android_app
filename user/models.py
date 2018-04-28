from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Business(models.Model):
    name = models.CharField(max_length=50)
    star = models.FloatField()
    attribute = models.CharField(max_length=200)
    

class Photo(models.Model):
    img_url = models.CharField(max_length=50)
    business = models.ForeignKey(Business)
    

class Comment(models.Model):
    business = models.ForeignKey(Business, default=None)
    user = models.ForeignKey(User, default=None)
    date = models.DateTimeField()
    text = models.CharField(max_length=200)
    star = models.FloatField()
    
    
class Recommend(models.Model):
    business = models.ForeignKey(Business, default=None)
    user = models.ForeignKey(User, default=None)

