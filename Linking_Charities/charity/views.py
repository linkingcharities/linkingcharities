from django.shortcuts import render
from rest_framework import generics
from charity.models import Charity, Volunteering
from charity.serializers import CharitySerializer, CharityCreateSerializer, VolunteeringSerializer
from rest_framework.permissions import AllowAny
import django_filters
from rest_framework import filters
from rest_framework.serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from django.contrib.auth.models import User
from django.db.models import Q
from account.models import *
from library import *

class IncomeFilter(django_filters.rest_framework.FilterSet):
    min_income = django_filters.NumberFilter(name="total_income", lookup_expr='gte')
    max_income = django_filters.NumberFilter(name="total_income", lookup_expr='lte')
    class Meta:
        model = Charity
        fields = ('id','name', 'target', 'type', 'min_income', 'max_income')

class ListCreateCharities(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Charity.objects.all().order_by('-donations')
    serializer_class = CharitySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,filters.SearchFilter,)
    filter_class = IncomeFilter

    def get(self, request):
        response = super(ListCreateCharities, self).get(self, request)
        return makeHttpResponse(response.data, status=response.status_code)

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
            return makeHttpResponse(new_data, status=HTTP_200_OK)
        User.object.delete(username=username)
        return makeHttpResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)

class DateFilter(django_filters.rest_framework.FilterSet):
    start_date = django_filters.DateFilter(name="start_date", lookup_expr='gte')
    end_date = django_filters.DateFilter(name="end_date", lookup_expr='lte')
    class Meta:
        model = Volunteering
        fields = ('id', 'charity','start_date', 'end_date')

class ListCreateVolunteering(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Volunteering.objects.all()
    serializer_class = VolunteeringSerializer
    filter_class = DateFilter

    def post(self, request, format=None):
        response = super(ListCreateVolunteering, self).post(request, format)
        return makeHttpResponse(response.data, status=response.status_code)

class updateCharity(APIView):
    permission_classes = [AllowAny]
    serializer_class = CharitySerializer

    def patch(self, request):
        data = request.data
        username = data.pop('username')
        account = User.objects.get(username=username)
        charity = CharityAccount.objects.get(account=account).charity
        serializer = CharitySerializer(charity, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return makeHttpResponse(serializer.data, status=HTTP_200_OK)
        return makeHttpResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UpdateVolunteering(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Volunteering.objects.all()
    serializer_class = VolunteeringSerializer

    def patch(self, request, pk):
        data = request.data
        vol = Volunteering.objects.get(pk=pk)
        serializer = VolunteeringSerializer(vol, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return makeHttpResponse(serializer.data, status=HTTP_200_OK)
        return makeHttpResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)
