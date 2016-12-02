from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import *
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from charity.models import *
from payment.models import *
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
from rest_framework.response import Response
from django.core import serializers

class MakePaymentAPIView(CreateAPIView):
    permission_classes = [AllowAny] 
    serializer_class = MakePaymentSerializer
    queryset = Payment.objects.all()
    
    def post(self, request, format=None):
        data = request.data
        paypal = data['business']
        
        payment = {
                    'username': data['item_name'],
                    'amount'  : float(data['payment_gross']),
                    'charity' : Charity.objects.filter(paypal=paypal).first().name,
                    'currency': data['mc_currency']
                   }
        p = Payment.objects.create(**payment)
        domain = request.get_host()
        domain = domain[:-5]
        return redirect('http://' + domain + '/thank-you/' + str(p.id))
        #return redirect("http://0.0.0.0:8080/thank-you/" + str(p.id))

class ShowPaymentAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShowPaymentSerializer
    http_method_names = ['get', 'post', 'head']
 
    def get_queryset(self):
        queryset = Payment.objects.all()
        user = self.request.query_params.get('username', None)
        payment = self.request.query_params.get('payment', None) 
        if user is not None:
          if payment is not None:
            queryset = queryset.filter(username=user, pk=payment)
            return queryset
          else:
            return queryset.filter(username=user)
        return Payment.objects.none()

    def post(self, request, format=None):
        print('reached')
        data = request.data
        user = data['username']
        payment = data['payment']
        #data = serializers.serialize('json', [ Payment.objects.get(username=user,pk=payment),])
        data = Payment.objects.get(username=user, pk=payment)
        return Response({'charity': data.charity, 'amount': data.amount }, status=HTTP_200_OK)
