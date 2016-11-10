from rest_framework import serializers
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
    username = CharField(required=True)
    payments = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            'username',
            'payments',
        ]
    
    def validate(self, data):
        username = data.get("username", None)
        if not username:
            raise ValidationError("Username is required.")
        payments = Payment.objects.filter(username=username)
        data['payments'] = payments
  
        return data
