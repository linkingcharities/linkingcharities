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
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from .serializers import *

class DonorAccountCreateAPIView(CreateAPIView):
    serializer_class = DonorAccountSerializer
    queryset = DonorAccount.objects.all()
    
class CharityAccountCreateAPIView(CreateAPIView):
    serializer_class = CharityAccountSerializer
    queryset = DonorAccount.objects.all()
