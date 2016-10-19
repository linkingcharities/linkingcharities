from django.conf.urls import url
from django.contrib import admin

from .views import (
    AccountCreateAPIView,
)

urlpatterns = [
    url(r'register/', AccountCreateAPIView.as_view(), name='register'),
]
