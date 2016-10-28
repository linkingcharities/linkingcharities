from django.conf.urls import include, url
from django.contrib import admin
from .views import (
    DonorAccountCreateAPIView,
    CharityAccountCreateAPIView,
)

urlpatterns = [
    url(r^'register/donor', DonorAccountCreateAPIView.as_view, name='donor_register')
    url(r^'register/charity', CharityAccountCreateAPIView.as_view, name='charity_register')
]
