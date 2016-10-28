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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import (
    AllowAny,
)
from .serializers import *


class DonorAccountCreateAPIView(CreateAPIView):
    serializer_class = DonorAccountSerializer
    queryset = DonorAccount.objects.all()
    
class CharityAccountCreateAPIView(CreateAPIView):
    serializer_class = CharityAccountSerializer
    queryset = DonorAccount.objects.all()

class DonorAccountLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = DonorAccountLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = DonorAccountLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class CharityAccountLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CharityAccountLoginSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CharityAccountLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
