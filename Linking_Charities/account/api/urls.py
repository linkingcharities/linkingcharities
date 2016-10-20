from django.conf.urls import url
from django.contrib import admin

from .views import (
    AccountCreateAPIView,
    AccountLoginAPIView,
)

urlpatterns = [
    url(r'register/', AccountCreateAPIView.as_view(), name='register'),
    url(r'login/', AccountLoginAPIView.as_view(), name='login',)
]
