# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 14:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_charityaccount_paypal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charityaccount',
            name='isCharity',
        ),
    ]
