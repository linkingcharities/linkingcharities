from django.shortcuts import render
from rest_framework import generics
from account.serializers import (
    DonorAccountSerializer,
    CharityAccountSerializer,
)
from account.models import (
    DonorAccount,
    CharityAccount,
)
from payment.models import Payment
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import (
    AllowAny,
)
from .serializers import *
from rest_framework.authtoken.models import Token
from django.core import serializers
from charity.serializers import CharitySerializer
from charity.models import Charity

class DonorAccountCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = DonorAccountSerializer
    queryset = DonorAccount.objects.all()
    
class CharityAccountCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CharityAccountSerializer
    queryset = CharityAccount.objects.all()

class AccountLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AccountLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = AccountLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class AccountInfoView(APIView):
    permission_classes = [AllowAny]
    serializer = CharityAccountSerializer
  
    def get(self, request):
        data = request.GET.get('username', None)
        if data is not None:
            account = None
            account = User.objects.get(username = data)
            donor = DonorAccount.objects.filter(account=account)
            #need to return token and username and payment
            if donor.exists():
                response = []
                payments = Payment.objects.filter(username=data)
                for payment in payments:
                    p = { 'username' : payment.username,
                          'charity'  : payment.charity,
                          'amount'   : payment.amount,
                          'currency' : payment.currency,
                          'date'     : payment.date }
                    response.append(p)
                return Response(response, status=HTTP_200_OK)
            charity_model = CharityAccount.objects.filter(account=account)
            #need to return charity info
            if charity_model.exists():
                charity = charity_model.first().charity
                response_data = {
                                 'name' : charity.name,
                                 'type' : charity.type,
                                 'register_id': charity.register_id,
                                 'area_served': charity.area_served,
                                 'total_income': charity.total_income,
                                 'target': charity.target,
                                 'description': charity.description,
                                 'paypal': charity.paypal
                                }
                return Response(response_data, status=HTTP_200_OK)
            return Response({}, status=HTTP_400_BAD_REQUEST)
            
        return Response({}, status=HTTP_400_BAD_REQUEST)
