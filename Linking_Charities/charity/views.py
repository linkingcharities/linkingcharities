from django.shortcuts import render
from rest_framework import generics
from charity.models import Charity, Volunteering
from charity.serializers import CharitySerializer, CharityCreateSerializer, VolunteeringSerializer
from rest_framework.permissions import AllowAny
import django_filters
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from django.contrib.auth.models import User
from django.db.models import Q
from account.models import *

class IncomeFilter(django_filters.rest_framework.FilterSet):
    min_income = django_filters.NumberFilter(name="total_income", lookup_expr='gte')
    max_income = django_filters.NumberFilter(name="total_income", lookup_expr='lte')
    class Meta:
        model = Charity
        fields = ('id','name', 'target', 'type', 'min_income', 'max_income')

class ListCreateCharities(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,)
    filter_fields = '__all__'
    filter_class = IncomeFilter

    def post(self, request, format=None):
        data = request.data
        username = data.pop('username')
        serializer = CharityCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            user = User.objects.filter(
                Q(username=username)
            )
            if not user.exists():
                raise ValidationError("No account provided.")
            charity_account = CharityAccount.objects.filter(
                Q(account=user)
            )
            if charity_account.exists():
                charity_account = charity_account.first()
            else:
                raise ValidationError("Charity account not provided.")
            charity_account.charity = Charity.objects.get(name=data['name'])
            charity_account.save()
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class DateFilter(django_filters.rest_framework.FilterSet):
    start_date = django_filters.DateFilter(name="start_date", lookup_expr='gte')
    end_date = django_filters.DateFilter(name="end_date", lookup_expr='lte')
    class Meta:
        model = Volunteering
        fields = ('id', 'name', 'charity', 'start_date', 'end_date')

        #TODO: FILTERING NAME BY FUZZY SEARCH, NOT NECESSARILY EXACT MATCH

class ListCreateVolunteering(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Volunteering.objects.all()
    serializer_class = VolunteeringSerializer
    filter_class = DateFilter

    def get(self, request):
        id = request.GET.get('id', None)
        if id is None:
            volunteering = Volunteering.objects.all()
            data = []
            for v in volunteering:
                d = {
                    'id': v.id,
                    'name': v.name,
                    'charity_name': v.charity.name,
                    'description': v.description,
                    'start_date': v.start_date,
                    'end_date': v.end_date,
                    'url': v.url }
                data.append(d)
            return Response(data, status=HTTP_200_OK)
        else:
            v = Volunteering.objects.filter(pk=id)
            if v.exists():
                v = v.first()
                d = {
                    'id': v.id,
                    'name': v.name,
                    'charity_name': v.charity.name,
                    'description': v.description,
                    'start_date': v.start_date,
                    'end_date': v.end_date,
                    'url': v.url }
                return Response(d, status=HTTP_200_OK)
            return Response('ID not found', status=HTTP_400_BAD_REQUEST)
