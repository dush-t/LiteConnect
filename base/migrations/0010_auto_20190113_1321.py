# Generated by Django 2.1.4 on 2019-01-13 13:21

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20190113_0807'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('publish_date', models.DateTimeField(default=datetime.datetime(2019, 1, 13, 13, 21, 14, 994879, tzinfo=utc))),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post_history',
            name='history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='base.Post'),
        ),
    ]
