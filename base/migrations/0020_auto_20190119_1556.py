# Generated by Django 2.1.4 on 2019-01-19 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20190119_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_picture',
            field=models.ImageField(default='LiteConnect/media/default.png', upload_to='propic'),
        ),
    ]
