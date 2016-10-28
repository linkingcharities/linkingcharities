from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class DonorAccount(models.Model):
    account = models.OneToOneField(User)

class CharityAccount(models.Model):
    account = models.OneToOneField(User)
    isCharity = models.BooleanField(default=True)
    description = models.TextField(max_length=1000, default="DEFAULT")
