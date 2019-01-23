from django import forms
from .models import Member, Post, Comment
import re
from django.core import validators
from django.forms import ModelForm

class Sign_up_form(forms.Form):
    username = forms.CharField(max_length=50)
    name = forms.CharField(max_length=50)
    email_id = forms.EmailField(max_length=60)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=30)

class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

class UserDataEditForm(ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'bio', 'profile_picture']

class Post_edit(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class PasswordChangeForm(forms.Form):
    Enter_Password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
    Confirm_Password = forms.CharField(widget=forms.PasswordInput(), max_length=30)
