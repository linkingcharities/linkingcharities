from django.shortcuts import render
from rest_framework import generics
from charity.models import Charity
from charity.serializers import CharitySerializer

class ListCreateCharities(generics.ListCreateAPIView):
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer
