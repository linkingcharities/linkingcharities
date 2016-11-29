from rest_framework import serializers
from django.core import serializers as to_json
from rest_framework.serializers import *
from .models import Payment, CURRENCY
from django.contrib.auth.models import User

class MakePaymentSerializer(serializers.ModelSerializer):
    username = CharField(required=True)
    charity = CharField(required=True)
    currency = ChoiceField(choices=CURRENCY)
    amount = IntegerField(required=True)
    date = DateTimeField(read_only=True)
    class Meta:
        model=Payment
        fields = [
            'username',
            'charity',
            'amount',
            'currency',
            'date',
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
     
    def validate(self, validated_data):
        user = validated_data['username']
        payment = validated_data['payment']
        return Payment.objects.get(username=user, payment=payment)
