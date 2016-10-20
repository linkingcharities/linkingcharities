from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from .serializers import *

class AccountCreateAPIView(CreateAPIView):
    serializer_class = AccountCreateSerializer
    queryset = User.objects.all()

class AccountLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AccountLoginSerializer
 
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = AccountLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
