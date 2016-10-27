from django.conf.urls import include, url
from django.contrib import admin
from charity.views import ListCreateCharities
from account.views import (
    DonorAccountCreateAPIView,
    CharityAccountCreateAPIView,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/charities', ListCreateCharities.as_view(), name='list_charities'),
    url(r'^api/donor/register', DonorAccountCreateAPIView.as_view(), name='donor_accounts'),
    url(r'^api/charity/register', CharityAccountCreateAPIView.as_view(), name='charity_accounts'),
]
