from django.urls import path
from . import views
import re
from django.conf.urls import url, include

urlpatterns = [
    path('news_feed', views.news_feed, name='news_feed'),
    path('profile/<str:username>', views.profile, name='user_profile'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('', views.sign_in, name='sign_in'),
    path('you', views.you, name='current_user_profile'),
    path('you/signout', views.sign_out, name='sign_out'),
    path('all_users', views.all_users, name='all_users'),
    path('profile/<str:username>/follow', views.follow_user, name='follow_user'),
    path('post/<int:key>', views.post_details, name="view_post"),
    path('edit', views.edit_profile_data, name='edit_profile_data'),
    path('post_edit/<int:key>', views.edit_post, name='edit_post'),
    path('post/<int:key>/edit_history', views.get_post_history, name='get_post_history'),
    path('post/<int:key>/delete', views.delete_post, name='delete_post'),
    path('change_pass', views.change_password, name='change_password'),
    path('profile/<str:username>/unfollow', views.unfollow_user, name='unfollow_user'),
    path('profile/<str:username>/subscribe', views.subscribe, name='subscribe'),
    path('profile/<str:username>/unsubscribe', views.unsubscribe, name='unsubscribe'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    ]