from rest_framework import serializers
from charity.models import Charity

class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ('charity_name', 'registered_id', 'description')
