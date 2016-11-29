from __future__ import unicode_literals

from django.db import models

CHARITY_TARGETS = (
    ('', 'Default'),
    ('C', 'Children/Young People'),
    ('E', 'Elderly/Old People'),
    ('D', 'People with disabilities'),
    ('R', 'People of particular ethnic/racial origin'),
    ('P', 'The general public'),
    ('O', 'Other')
)
CHARITY_PURPOSE = (
    ('','Default'),
    ('G', 'General Charitable Purposes'),
    ('E', 'Education/Training'),
    ('H', 'Advancement of Health/Saving Lives'),
    ('D', 'Disability'),
    ('P', 'Prevention or Relief of Poverty'),
    ('O', 'Overseas Aid/Famine Relief'),
    ('R', 'Religious Activities'),
    ('C', 'Arts/Culture/Heritage/Science'),
    ('S', 'Amateur Sport'),
    ('AN', 'Animals'),
    ('EN', 'Environment'),
    ('EC', 'Economic/Community Development/Employment'),
    ('A', 'Armed Forces'),
    ('HR', 'Human Rights/Equality'),
    ('RE', 'Recreation'),
    ('AH', 'Accommodation/Housing'),
    ('OT', 'Other')
)


class Charity(models.Model):
    name = models.CharField(max_length=100, default='DEFAULT')
    type = models.CharField(max_length=2, choices=CHARITY_PURPOSE)
    register_id = models.IntegerField(default=0, unique=True)
    area_served = models.CharField(max_length=100, default='DEFAULT')
    total_income = models.IntegerField(default=0)
    target = models.CharField(max_length=1, choices=CHARITY_TARGETS)
    logo = models.CharField(max_length=1000, default='DEFAULT')
    description = models.TextField()
    paypal = models.CharField(max_length=100, default='DEFAULT')

    def __str__(self):
        return self.name


class Volunteering(models.Model):
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    url = models.CharField(max_length=300, default='DEFAULT')

    def __str__(self):
        return self.charity + self.url
    
