from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from charity.models import Charity

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class DonorAccount(models.Model):
    account = models.OneToOneField(User)

class CharityAccount(models.Model):
    account = models.OneToOneField(User)
    paypal = models.CharField(max_length=100, default="DEFAULT")
    description = models.TextField(max_length=1000, default="DEFAULT")
    charity = models.ForeignKey(Charity, null=True, blank=True, default=None)
