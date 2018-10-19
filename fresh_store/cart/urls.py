from django.conf.urls import url

from cart import views

urlpatterns = [
    url('^add_cart/', views.add_cart, name='add_cart'),
    url('^cart/', views.cart, name='cart'),
    url('^cart_updata/', views.cart_updata, name='cart_updata'),
    url('^cart_check_all/', views.cart_check_all, name='cart_check_all'),
    url('^cart_check_one/', views.cart_check_one, name='cart_check_one')
]