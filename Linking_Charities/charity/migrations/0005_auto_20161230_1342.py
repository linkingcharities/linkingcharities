# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-30 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0004_auto_20161230_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charity',
            name='paypal',
            field=models.CharField(default='DEFAULT', max_length=100, unique=True),
        ),
    ]