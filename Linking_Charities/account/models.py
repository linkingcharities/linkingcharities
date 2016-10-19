from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    account = models.OneToOneField(User)
    isCharity = models.BooleanField(default=False)

    @property
    def username(self):
        return User.get_username()
  
