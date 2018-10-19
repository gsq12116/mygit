from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'^detail/(?P<g_id>\d+)/', views.detail, name='detail'),
]