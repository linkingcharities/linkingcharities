from rest_framework import serializers
from rest_framework.serializers import *
from charity.models import Charity, Volunteering
from rest_framework.authtoken.models import Token

class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ('id', 'name', 'register_id', 'type','description', 'target',
                  'total_income', 'paypal')

class CharityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = [ 'name', 'register_id', 'type', 'description', 'target', 'total_income',
                   'paypal']

    def validate(self, validated_data):
        charity = Charity.objects.create(**validated_data)
        return charity


class VolunteeringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteering
        fields = ('id', 'name', 'charity', 'description', 'start_date', 'end_date', 'url')
