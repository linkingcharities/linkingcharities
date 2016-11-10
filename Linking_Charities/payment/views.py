from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import *
from rest_framework.response import Response

class MakePaymentAPIView(CreateAPIView):
    permission_classes = [AllowAny] 
    serializer_class = MakePaymentSerializer
    queryset = Payment.objects.all()

class ShowPaymentAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ShowPaymentSerializer
 
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ShowPaymentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
