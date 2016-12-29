from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

CURRENCY = (
    ('USD', 'US Dollar'),
    ('GBP', 'GB Sterling'),
)

class Payment(models.Model):
    account_id = models.IntegerField(default=0, null=True)
    paypal = models.CharField(max_length=100, default="DEFAULT")
    charity_id = models.IntegerField(default=0, null=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    amount = models.IntegerField(default=0, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY)
