# Generated by Django 2.1.4 on 2019-01-19 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_auto_20190117_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='bio',
            field=models.CharField(blank=True, max_length=280),
        ),
        migrations.AlterField(
            model_name='member',
            name='profile_picture',
            field=models.ImageField(default='/home/mr_dush__t/django-dush-t/LiteConnect/LiteConnect/media/default.png', upload_to='propic'),
        ),
    ]