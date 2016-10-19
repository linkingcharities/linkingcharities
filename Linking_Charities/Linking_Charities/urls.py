from django.conf.urls import include, url
from django.contrib import admin
from charity.views import ListCreateCharities

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/charities', ListCreateCharities.as_view(), name='list_charities'),
]
