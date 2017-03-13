# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 14:44
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chain', '0008_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('about', models.CharField(blank=True, max_length=400)),
                ('doc', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('image', models.CharField(blank=True, default=b'http://www.hit4hit.org/img/login/user-icon-6.png', max_length=400)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]