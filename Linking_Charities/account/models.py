from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class DonorAccount(models.Model):
    account = models.OneToOneField(User)

class CharityAccount(models.Model):
    account = models.OneToOneField(User)
    isCharity = models.BooleanField(default=True)
    description = models.TextField(max_length=1000, default="DEFAULT")
