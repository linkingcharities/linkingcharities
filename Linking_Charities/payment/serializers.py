from rest_framework import serializers
from django.core import serializers as to_json
from rest_framework.serializers import *
from .models import Payment
from django.contrib.auth.models import User
import datetime

class MakePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields = [
            'username',
            'charity',
            'amount',
            'currency',
         ]
    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        return payment

class ShowPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'username',
            'charity',
            'date',
            'amount',
            'currency',
        ]
    
