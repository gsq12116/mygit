from django.conf.urls import url

from home import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^list/(?P<g_type>\d+)/', views.goods_list, name='list'),
]