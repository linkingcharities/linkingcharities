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
        data = request.GET.get('account_id', None)
        if data is not None:
            account = User.objects.get(pk=data)
            donor = DonorAccount.objects.filter(account=account)
            # need to return token and username and payment
            if donor.exists():
                payments = Payment.objects.filter(account_id=account.id)
                resp_payments = []
                for payment in payments:
                    charity = Charity.objects.get(id=payment.charity_id)
                    p = {'account_id': payment.account_id,
                         'charity_id': payment.charity_id,
                         'amount': payment.amount,
                         'currency': payment.currency,
                         'date': payment.date,
                         'charity': charity.name
                         }
                    resp_payments.append(p)

                response = {
                    'is_charity': False,
                    'payments': resp_payments
                }
                return Response(response, status=HTTP_200_OK)

            charity_accounts = CharityAccount.objects.filter(account=account)
            if charity_accounts.exists():
                charity_account = charity_accounts.first()

                charity = charity_account.charity
                charity_data = {
                    'name': charity.name,
                    'type': charity.type,
                    'register_id': charity.register_id,
                    'area_served': charity.area_served,
                    'total_income': charity.total_income,
                    'target': charity.target,
                    'description': charity.description,
                    'paypal': charity.paypal
                }

                response = {
                    'is_charity': True,
                    'charity_id': charity_account.charity_id,
                    'payments': [],
                    'charity': charity_data
                }
                # Can add in associated payments here
                return Response(response, status=HTTP_200_OK)
            return Response({}, status=HTTP_400_BAD_REQUEST)

        return Response({}, status=HTTP_400_BAD_REQUEST)
