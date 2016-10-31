from django.shortcuts import render
from django.core.urlresolvers import reverse
from paypal.standard.forms import PayPalPaymentsForm

from rest_framework.generics import CreateAPIView
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class PaypalMakePaymentAPIView(CreateAPIView):
    serializer_class = PaypalViewPaymentSerializer
    queryset = PaypalPayment.objects.all()

class PaypalShowPaymentAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PaypalPaymentSerializer
 
    def post(self, request, *args, **kwargs):
        return None
