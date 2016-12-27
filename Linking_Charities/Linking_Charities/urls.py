from django.conf.urls import include, url
from django.contrib import admin
from charity.views import ListCreateCharities, ListCreateVolunteering, updateCharity
from payment.views import *
from account.views import (
    DonorAccountCreateAPIView,
    CharityAccountCreateAPIView,
    AccountLoginAPIView,
    AccountInfoView
)
from payment.views import (
    MakePaymentAPIView,
    ShowPaymentAPIView,
)
from rest_framework.authtoken import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/charities', ListCreateCharities.as_view(), name='list_charities'),
    url(r'^api/update_charity', updateCharity.as_view(), name='update_charity'),
    url(r'^api/donor/register', DonorAccountCreateAPIView.as_view(), name='donor_accounts_create'),
    url(r'^api/login', AccountLoginAPIView.as_view(), name='login'),
    url(r'^api/charity/register', CharityAccountCreateAPIView.as_view(), name='charity_accounts_create'),
    url(r'^api/account_info/$', AccountInfoView.as_view(), name='get_account_information'),
    url(r'^api/auth_token', views.obtain_auth_token, name='auth token api'),
    url(r'^api/show_payment', ShowPaymentAPIView.as_view(), name='see_payment'),
    url(r'^api/make_payment', MakePaymentAPIView.as_view(), name='make_payment'),
    url(r'^api/volunteering', ListCreateVolunteering.as_view(), name='list_volunteering'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
