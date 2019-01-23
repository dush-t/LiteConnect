from django.shortcuts import render, redirect, get_object_or_404
from .models import Member, Post, Comment, Post_history
from .forms import Sign_up_form, LoginForm, PostForm, CommentForm, UserDataEditForm, Post_edit, PasswordChangeForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from operator import attrgetter #Is this magic?
from django.contrib.auth.decorators import login_required
import os
import sendgrid
from sendgrid.helpers.mail import *
from django.core.mail import send_mail
from . import config



def create_member(request, user):
    if Member.objects.filter(user=user).exists():
        pass
    else:
        if Member.objects.filter(email=user.email).exists():
            return HttpResponse("This google account is already registered with this account. Please sign in from the login page")
        else:
            new_member = Member(username=user.username, name="Your Name Here", bio="Click on 'Edit profile details' to change your name and this bio",  email=user.email, user=user)
            new_member.save()
        


@login_required(login_url='/')
def news_feed(request):
    current_user = request.user
    create_member(request, current_user)
    current_member = Member.objects.get(user = current_user)
    following_list = current_member.follows.all()
    post_list = []
    user_list = Member.objects.all()

#The below code will take the posts by all the users you have followed, put them in a list and arrange them with date.
    for member in following_list:
        for post in member.Post.all():
            post_list.append(post)
    ordered_post_list = sorted(post_list, key=attrgetter('publish_date'), reverse=True)  #This piece of code sorts the list of posts with date
    
    return render(request, 'base/news_feed.html', {
        'post_list':ordered_post_list,
        'user_list':user_list
        })

def edit_profile_data(request):
    current_user = request.user
    create_member(request, current_user)
    current_member = Member.objects.get(user = current_user)
    if request.method == 'POST':
        form = UserDataEditForm(request.POST, request.FILES)
        if form.is_valid():
            
            new_name = form.cleaned_data.get('name')
            new_bio = form.cleaned_data.get('bio')
            
            current_member.name = new_name
            current_member.bio = new_bio
            current_member.profile_picture = form.cleaned_data.get('profile_picture')
            current_member.save()
            
            return redirect('/you')
    else:
        form = UserDataEditForm(instance=current_member)
        return render(request, 'base/edit_profile_data.html', {'form':form})


def delete_post(request, key):
    current_user = request.user
    create_member(request, current_user)
    current_member = Member.objects.get(user=current_user)
    current_post = Post.objects.get(pk=key)
    
    current_post.delete()
    return redirect('/you')


def profile(request, username):
    current_user = request.user
    create_member(request, current_user)
    current_member = Member.objects.get(user=current_user)
    user_viewed = get_object_or_404(Member, username=username)

    if current_member == user_viewed:
        return redirect('/you')
    else:
        post_list = user_viewed.Post.all().order_by('-publish_date')
        followers_list = user_viewed.followers.all()
        following_list = user_viewed.follows.all()
        subscriber_list = user_viewed.subscriber.all()
        if current_member in followers_list:
            is_following = True
        else:
            is_following = False

        if current_member in subscriber_list:
            subscribed=True
        else:
            subscribed=False

        return render(request, 'base/profile.html',{
                'user_viewed':user_viewed, 
                'post_list':post_list,
                'followers_list':followers_list,
                'following_list':following_list,
                'followercount':len(followers_list),
                'followingcount':len(following_list),
                'is_following':is_following,
                'subscribercount':len(subscriber_list),
                'subscribed':subscribed
                })
    


def post_details(request, key):
    current_user = request.user
    create_member(request, current_user)
    current_member = Member.objects.get(user=current_user)
    current_post = get_object_or_404(Post, pk=key)
    post_url = str(key)
    redir_url = '/post/'+str(key)
    comment_list = current_post.Comment.all().order_by('-publish_date')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('comment')
            new_comment = Comment(author=current_member, content=content, publish_date=timezone.now(), post=current_post)
            new_comment.save()
            return redirect(redir_url)

    else:
        form = CommentForm()
        return render(request, 'base/post_details.html', {
        'form':form,
        'post':current_post,
        'post_url':post_url,
        'comment_list':comment_list,
        'current_member':current_member
        })

def change_password(request):
    current_user = request.user
    create_member(request, current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('Enter_Password')
            password_repeat = form.cleaned_data.get('Confirm_Password')
            if password == password_repeat:
                current_user.set_password(password)
                current_user.save()
                return redirect('/')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('/change_pass')
    else:
        form = PasswordChangeForm()
        return render(request, 'base/change_pass.html', {'form':form})


def edit_post(request, key):
    current_user = request.user
    create_member(request, current_user)
    current_member = Member.objects.get(user=current_user)
    current_post = Post.objects.get(pk=key)
    post_url = str(key)
    redir_url = '/post/'+str(key)

    if request.method == 'POST':
        form = Post_edit(request.POST)
        if form.is_valid():
            if current_post.author == current_member:
                new_title = form.cleaned_data.get('title')
                new_content = form.cleaned_data.get('content')
                older_post = Post_history(title=current_post.title, content=current_post.content, publish_date=timezone.now(), history=current_post)
                older_post.save()
                current_post.title = new_title
                current_post.content = new_content
                current_post.save()

                return redirect(redir_url)
            else:
                messages.error(request, "You cannot edit this post because this post is not yours") #Just in case I fucked up somewhere.
                return redirect(redir_url)
    else:
        form = Post_edit(instance = current_post)
        return render(request, 'base/post_edit.html', {'form':form, 'post':current_post})


def get_post_history(request, key):
    current_post = Post.objects.get(pk=key)
    older_posts = current_post.post.all().order_by('-publish_date')

    return render(request, 'base/post_history.html', {'older_posts':older_posts})

@login_required(login_url='/')
def you(request):
    current_user = request.user
    create_member(request, current_user)
    current_member= Member.objects.get(user = current_user)
    post_list = current_member.Post.all().order_by('-publish_date')
    followers_list = current_member.followers.all()
    following_list = current_member.follows.all()
    subscriber_list = current_member.subscriber.all()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            author = current_member
            new_post = Post.objects.create(author=current_member, title=title, content=content, publish_date=timezone.now())
            new_post.save()
            url = "127.0.0.1:8000/post/" + str(new_post.pk)

            #This for loop will send emails to all the subscribers of current_member
            for member in subscriber_list:
                sg = sendgrid.SendGridAPIClient(apikey=config.sendgrid_api_key)
                from_email = Email("f20180179@pilani.bits-pilani.ac.in")
                to_email = Email(str(member.email))
                subject = current_member.username + " - " + title
                content = Content("text/plain", "Check out this new post by " + current_member.username + " - " + url)
                mail = Mail(from_email, subject, to_email, content)
                response = sg.client.mail.send.post(request_body=mail.get())
                print(response.status_code)
                print(response.body)
                print(response.headers)
                print(to_email)

            return redirect('/you')
    else:
        form = PostForm()    
        return render(request, 'base/you.html',{
            'current_user':current_member, 
            'form':form,
            'post_list':post_list,
            'followers_list':followers_list,
            'following_list':following_list,
            'followercount':len(followers_list),
            'followingcount':len(following_list),
            'subscribercount':len(subscriber_list)
            })

@login_required(login_url='/')
def all_users(request):
    user_list = Member.objects.exclude(user=request.user)
    return render(request, 'base/all_users.html', {'user_list':user_list})


def sign_up(request):
    if request.method == 'POST':
        form = Sign_up_form(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            if User.objects.filter(username=user_name).exists():
                messages.error(request, "Sorry, username already taken")
                return redirect('/sign_up')
            password = form.cleaned_data.get('password')
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email_id')
            if Member.objects.filter(email=email):
                messages.error(request, "This email address is already registered on this site")
                return redirect("/sign_up")

            new_user = User.objects.create_user(username=user_name, password=password)
            new_user.save()

            member = Member(username=user_name, name=name, user=new_user, email=email)
            member.save()
            return redirect('/')
        else:
            form=Sign_up_form()
            messages.error(request, 'Please check your BITS ID')
            return render(request, 'base/sign_up.html', {'form':form})
    else:
        form=Sign_up_form()
        return render(request, 'base/sign_up.html', {'form':form})



def sign_in(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                user_name = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                current_user = authenticate(username=user_name, password=password)
                if current_user:
                    login(request, current_user)
                    current_user = request.user
                    create_member(request, current_user)
                    current_member= Member.objects.get(user = current_user)
                    messages.success(request, 'Welcome to LiteConnect')
                    return redirect('/you')
                    #return render(request, 'base/you.html', {'current_user':current_member})
                else:
                    messages.error(request, 'Please check your login credentials')
                    return redirect('/')
            else:
                messages.error(request, "Please check the data you entered")

        else:
            form = LoginForm()
            return render(request, 'base/sign_in.html', {'form':form})
    else:
        return redirect('/you')



def sign_out(request):
    logout(request)
    return redirect('/')


def follow_user(request, username):
    current_user = request.user
    create_member(request, current_user)
    current_member = Member.objects.get(user=current_user)
    user_viewed = Member.objects.get(username=username)

    current_member.follows.add(user_viewed)
    url = '/profile/' + username 
    return redirect(url)

def unfollow_user(request, username):
    current_user = request.user
    create_member(request, current_user)
    current_member = Member.objects.get(user=current_user)
    user_viewed = Member.objects.get(username=username)

    user_viewed.followers.remove(current_member)
    url = '/profile/' + username 
    return redirect(url)

def subscribe(request, username):
    current_user = request.user
    create_member(request, current_user)
    current_member = Member.objects.get(user=current_user)
    user_viewed = Member.objects.get(username=username)

    current_member.subscribed_to.add(user_viewed)
    url = '/profile/' + username 
    return redirect(url)

def unsubscribe(request, username):
    current_user = request.user
    create_member(request, current_user)
    current_member = Member.objects.get(user=current_user)
    user_viewed = Member.objects.get(username=username)

    user_viewed.subscriber.remove(current_member)
    url = '/profile/' + username
    return redirect(url)

