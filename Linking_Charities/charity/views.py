from django.shortcuts import render
from rest_framework import generics
from charity.models import Charity
from charity.serializers import CharitySerializer
from rest_framework.permissions import AllowAny
import django_filters
from rest_framework import filters

class IncomeFilter(django_filters.rest_framework.FilterSet):
    min_income = django_filters.NumberFilter(name="total_income", lookup_expr='gte')
    max_income = django_filters.NumberFilter(name="total_income", lookup_expr='lte')
    class Meta:
        model = Charity
        fields = ('name', 'type', 'min_income', 'max_income')

class ListCreateCharities(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,)
    filter_fields = '__all__'
    search_fields = ('name',)
    filter_class = IncomeFilter
