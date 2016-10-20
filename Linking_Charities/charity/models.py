from __future__ import unicode_literals

from django.db import models


class Charity(models.Model):
    name = models.CharField(max_length=100, default='DEFAULT')
    type = models.CharField(max_length=50, default='DEFAULT')
    register_id = models.IntegerField(default=0)
    area_served = models.CharField(max_length=100, default='DEFAULT')  # needs to resolve list issues
    total_income = models.IntegerField(default=0)
    target = models.CharField(max_length=100, default='DEFAULT')  # same as above
    logo = models.CharField(max_length=1000, default='DEFAULT')
    description = models.CharField(max_length=5000, default='DEFAULT')

    def __str__(self):
        return self.name
