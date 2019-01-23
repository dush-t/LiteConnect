from django.contrib import admin
from .models import Member, Post
from openpyxl import Workbook
from openpyxl import load_workbook
from django.utils import timezone


def generate_stat(modeladmin, request, queryset):
    filepath="/home/mr_dush__t/django-dush-t/LiteConnect/LiteConnect/data.xlsx"
    
    data = load_workbook(filepath)
    sheet = data.active
    empty_row = ("","","","","","")
    time_row = ("", "", "DATA FETCHED ON -", str(timezone.now()), "", "")
    title_row = ("USERNAME", "NAME", "FOLLOWERS", "FOLLOWING", "POST COUNT", "BIO")
    sheet.append(empty_row)
    sheet.append(empty_row)
    sheet.append(empty_row)
    sheet.append(time_row)
    sheet.append(title_row)
    for member in queryset:
        username = member.username
        name = member.name
        followercount = member.followers.all().count()
        followingcount = member.follows.all().count()
        postcount = member.Post.all().count()
        bio = member.bio

        data_row = (username, name, followercount, followingcount, postcount, bio)
        sheet.append(data_row)
        data.save(filepath)
    generate_stat.short_description = "Generate user statistics sheets"


class DataAdmin(admin.ModelAdmin):
    actions = [generate_stat, ]


admin.site.register(Member, DataAdmin)
admin.site.register(Post)