from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^login/', views.login, name='login'),
	url(r'^signup/', views.signup, name='signup'),
	url(r'^$', views.index, name='index'),
]
