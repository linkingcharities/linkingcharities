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
from django.conf import settings


class MakePaymentAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = MakePaymentSerializer
    queryset = Payment.objects.all()

    def post(self, request, format=None):
        data = request.data
        print(request)
        paypal = data['business']
        charity = Charity.objects.get(paypal=paypal)
        charity.donations = charity.donations + int(float(data['mc_gross']))
        charity.save()

        if settings.TESTING:
            domain = '0.0.0.0:8080'
        else:
            domain = request.get_host()
            domain = domain[:-5]
        if data['item_name'] == 'donation':
            return redirect('http://' + domain + '/charities/')
        user = User.objects.get(pk=data['item_name'])
        payment = {
            'account': user,
            'paypal': data['business'],
            'amount': float(data['mc_gross']),
            'charity': charity,
            'currency': data['mc_currency']
        }
        p = Payment.objects.create(**payment)
        return redirect('http://' + domain + '/thank-you/' + str(p.id))


class ShowPaymentAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PaymentSerializer
    http_method_names = ['get', 'post', 'head']

    def get(self, request):
        queryset = Payment.objects.all()
        account_id = self.request.query_params.get('account_id', None)
        account = User.objects.filter(id=account_id)
        if account.exists():
            account = account.first()
        else:
            return makeHttpResponse([], status=HTTP_400_BAD_REQUEST)
        charity = self.request.query_params.get('charity', None)
        return_data = None
        if charity is not None:
            return_data = queryset.filter(charity_id=account_id)
        else:
            return_data = queryset.filter(account_id=account.id)
        ret = []
        for payment in return_data:
            ret.append({
                'account_id': payment.account.id,
                'paypal': payment.paypal,
                'charity_id': payment.charity.id,
                'date': str(payment.date),
                'amount': payment.amount,
                'currency': payment.currency
            })
        return makeHttpResponse(ret, status=HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        user = data['username']
        payment = data['payment']
        account = User.objects.filter(username=user)
        if account.exists():
            account = account.first()
        else:
            return Payment.objects.none()
        data = Payment.objects.get(account=account, pk=payment)
        return makeHttpResponse({'charity': data.charity.name, 'amount': data.amount}, HTTP_200_OK)
