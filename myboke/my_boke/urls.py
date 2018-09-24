"""new python"""
from django.conf.urls import url

from my_boke import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^info/(?P<a_id>\d+)/', views.info, name='info'),
]