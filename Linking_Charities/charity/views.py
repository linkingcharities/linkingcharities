from django.shortcuts import render
from rest_framework import generics
from charity.models import Charity
from charity.serializers import CharitySerializer
from rest_framework.permissions import AllowAny

class ListCreateCharities(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer
