from __future__ import unicode_literals

from django.db import models

class Charity(models.Model):
  charity_name = models.CharField(max_length=100, default='DEFAULT')
  charity_type = models.CharField(max_length=50, default='DEFAULT')
  charity_register_id = models.IntegerField(default=0)
  charity_area_served = models.CharField(max_length=100, default='DEFAULT') #needs to resolve list issues
  charity_total_income = models.IntegerField(default=0)
  charity_target = models.CharField(max_length=100, default='DEFAULT') #same as above
  charity_logo = models.CharField(max_length=1000, default='DEFAULT')
  charity_description = models.CharField(max_length=5000, default='DEFAULT')
  def __str__(self):
    return self.charity_name



  
