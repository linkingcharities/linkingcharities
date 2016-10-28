from __future__ import unicode_literals

from django.db import models

class PaypalPayment(models.Model):
    username = models.CharField(max_length=100, default="DEFAULT")
    business = models.CharField(max_length=100, default="DEFAULT")
    amount = models.IntegerField(default=0, null=True)
    item_name = models.CharField(max_length=100, default="DEFAULT")
    invoice = models.IntegerField(default=0, null=True)
    notify_url = models.CharField(max_length=100, default="DEFAULT")
    return_url = models.CharField(max_length=100, default="DEFAULT")
    cancel_return = models.CharField(max_length=100, default="DEFAULT")
    
