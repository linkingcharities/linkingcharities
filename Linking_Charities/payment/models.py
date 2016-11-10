from __future__ import unicode_literals
from datetime import datetime

from django.db import models

class Payment(models.Model):
    CURRENCY = (
        ('USD', 'US Dollar'),
        ('GBP', 'GB Sterling')
    )
    username = models.CharField(max_length=100, default="DEFAULT")
    charity = models.CharField(max_length=100, default="DEFAULT")
    date = models.DateTimeField(default=datetime.now, blank=True)
    amount = models.IntegerField(default=0, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY)
