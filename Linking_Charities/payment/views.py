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
from django.contrib.auth.models import User
from django.db.models.functions import TruncYear
from library import *


class MakePaymentAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = MakePaymentSerializer
    queryset = Payment.objects.all()

    def post(self, request, format=None):
        data = request.data
        paypal = data['business']
        charity = Charity.objects.filter(paypal=paypal).first()
        charity.donations = charity.donations + int(float(data['mc_gross']))
        charity.save()
        payment = {
                    'account_id': data['item_name'],
                    'paypal' : data['business'],
                    'amount'  : float(data['mc_gross']),
                    'charity_id' : charity.id,
                    'currency': data['mc_currency']
                   }
        p = Payment.objects.create(**payment)
        domain = request.get_host()
        domain = domain[:-5]
        #return redirect('http://' + domain + '/thank-you/' + str(p.id))
        return redirect("http://0.0.0.0:8080/thank-you/" + str(p.id))

class ShowPaymentAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShowPaymentSerializer
    http_method_names = ['get', 'post', 'head']

    def get_queryset(self):
        queryset = Payment.objects.all()
        user = self.request.query_params.get('username', None)
        account = User.objects.filter(username=user)
        if account.exists():
          account = account.first()
        else:
          return Payment.objects.none()
        payment = self.request.query_params.get('payment', None)
        if payment is not None:
          queryset = queryset.filter(account_id=account.id, pk=payment)
          return queryset
        else:
          return queryset.filter(account_id=account.id)
        return Payment.objects.none()

    def post(self, request, format=None):
        data = request.data
        user = data['username']
        payment = data['payment']
        account = User.objects.filter(username=user)
        if account.exists():
          account = account.first()
        else:
          return Payment.objects.none()
        data = Payment.objects.get(account_id=account.id, pk=payment)
        charity = Charity.objects.get(pk=data.charity_id)
        return makeHttpResponse({'charity': charity.name, 'amount': data.amount }, HTTP_200_OK)
