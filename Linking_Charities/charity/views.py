from django.shortcuts import render
from rest_framework import generics
from charity.models import Charity
from charity.serializers import CharitySerializer
from rest_framework.permissions import AllowAny
import django_filters

class ListCreateCharities(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('type','name',)
