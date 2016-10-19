from django.shortcuts import render
from rest_framework import generics
from testapp.models import Charity
from testapp.serializers import CharitySerializer

class ListCreateCharities(generics.ListCreateAPIView):
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer
