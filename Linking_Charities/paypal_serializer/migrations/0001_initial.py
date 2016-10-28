# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaypalPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.CharField(default='DAFAULT', max_length=100)),
                ('amount', models.IntegerField(default=0, null=True)),
                ('item_name', models.CharField(default='DEFAULT', max_length=100)),
                ('invoice', models.IntegerField(default=0, null=True)),
                ('notify_url', models.CharField(default='DEFAULT', max_length=100)),
                ('return_url', models.CharField(default='DEFAULT', max_length=100)),
                ('cancel_return', models.CharField(default='DEFAULT', max_length=100)),
            ],
        ),
    ]
