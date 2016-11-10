from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import *
from rest_framework.response import Response

class MakePaymentAPIView(CreateAPIView):
    permission_classes = [AllowAny] 
    serializer_class = MakePaymentSerializer
    queryset = Payment.objects.all()

class ShowPaymentAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShowPaymentSerializer
    http_method_names = ['get', 'head']
 
    def get_queryset(self):
        queryset = Payment.objects.all()
        user = self.request.query_params.get('username', None)
        
        if user is not None:
            queryset = queryset.filter(username=user)
            return queryset
        return Payment.objects.none()
