from rest_framework import serializers
from rest_framework.serializers import *
from .models import PaypalPayment

class PaypalPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=PaypalPayment
        fields = [
            'username',
            'business',
            'amount',
            'item_name',
            'invoice',
            'notify_url',
            'return_url',
            'cancel_return',
        ]
    def create(self, validated_data):
        payment = PaypayPayment.objects.create(**validated_data)
        return payment


