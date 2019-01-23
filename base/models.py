from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.conf import settings
from django.utils import timezone
import re
import os
# Create your models here.

class Member(models.Model):
    username = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    number_of_followers = models.IntegerField(default=0)
    bio = models.CharField(max_length=280, blank=True)
    follows = models.ManyToManyField("self", related_name='followers', symmetrical=False, blank=True)
    subscribed_to = models.ManyToManyField("self", related_name='subscriber', symmetrical=False, blank=True)
    profile_picture = models.ImageField(upload_to='propic', null=True, blank=True)
    email = models.EmailField(max_length=60, blank=True)

    def __str__(self):
        return self.username
        
    

class Post(models.Model):
    author = models.ForeignKey(Member, on_delete=models.CASCADE, blank=False, related_name='Post')
    title = models.CharField(max_length=100, default="My Post")
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    comment_count = models.IntegerField(default=0)
    is_edited = models.BooleanField(default = False)

    def __str__(self):
        return self.title
        
class Post_history(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    history = models.ForeignKey(Post, on_delete=models.CASCADE, blank = False, related_name='post')


class Comment(models.Model):
    author = models.ForeignKey(Member, on_delete=models.CASCADE, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=False, related_name='Comment')
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    

