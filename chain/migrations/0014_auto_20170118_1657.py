# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-18 11:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chain', '0013_auto_20170118_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='description',
        ),
        migrations.RemoveField(
            model_name='node',
            name='gateway_name',
        ),
        migrations.RemoveField(
            model_name='node',
            name='image',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='image',
        ),
        migrations.DeleteModel(
            name='Gateway',
        ),
    ]
