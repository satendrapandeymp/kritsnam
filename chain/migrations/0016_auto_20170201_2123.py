# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 15:53
from __future__ import unicode_literals

from django.db import migrations
import django_unixdatetimefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('chain', '0015_auto_20170128_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='doc',
            field=django_unixdatetimefield.fields.UnixDateTimeField(),
        ),
    ]
