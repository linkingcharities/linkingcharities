from django.conf.urls import include, url
from django.contrib import admin
from charity.views import ListCreateCharities
from account.views import ListCreateAccount

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/charities', ListCreateCharities.as_view(), name='list_charities'),
    url(r'^api/account', include("account.api.urls"), name='user_accounts')
]
