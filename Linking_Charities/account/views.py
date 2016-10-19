from django.shortcuts import render
from rest_framework import generics
from account.serializers import AccountSerializer
from account.models import Account

class ListCreateAccount(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
