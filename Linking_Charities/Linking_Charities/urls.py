from django.conf.urls import include, url
from django.contrib import admin
from charity.views import ListCreateCharities
from account.views import (
    DonorAccountCreateAPIView,
    DonorAccountLoginAPIView,
    CharityAccountCreateAPIView,
    CharityAccountLoginAPIView,
)
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/charities', ListCreateCharities.as_view(), name='list_charities'),
    url(r'^api/donor/register', DonorAccountCreateAPIView.as_view(), name='donor_accounts_create'),
    url(r'^api/donor/login', DonorAccountLoginAPIView.as_view(), name='donor_login'),
    url(r'^api/charity/register', CharityAccountCreateAPIView.as_view(), name='charity_accounts_create'),
    url(r'^api/charity/login', CharityAccountLoginAPIView.as_view(), name='charity_login'),
    url(r'^api/auth_token', views.obtain_auth_token, name='auth token api')
]
