# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-18 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chain', '0010_auto_20170107_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='data',
            field=models.FloatField(default=1.7777),
        ),
    ]
