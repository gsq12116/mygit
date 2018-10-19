"""new python"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from home import views

urlpatterns = [
    url(r'^index/', login_required(views.index), name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', login_required(views.logout), name='logout'),
]