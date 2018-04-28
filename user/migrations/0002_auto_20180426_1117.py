# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-26 03:17
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='business',
        ),
        migrations.AddField(
            model_name='comment',
            name='business',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user.Business'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='data',
            field=models.DateTimeField(verbose_name=datetime.datetime(2018, 4, 26, 3, 17, 57, 733375, tzinfo=utc)),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='recommend',
            name='business',
        ),
        migrations.AddField(
            model_name='recommend',
            name='business',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user.Business'),
        ),
        migrations.RemoveField(
            model_name='recommend',
            name='user',
        ),
        migrations.AddField(
            model_name='recommend',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
