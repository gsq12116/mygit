from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from goods import views

urlpatterns = [
    # 商品分类列表
    url(r'^goods_category_list/', login_required(views.goods_category_list), name='goods_category_list'),
    # 分类编辑页面
    url(r'^goods_category_detail/(?P<id>\d+)/', login_required(views.goods_category_detail), name='goods_category_detail'),
    # 商品列表
    url(r'^goods_list/', login_required(views.goods_list), name='goods_list'),
    # 添加商品界面
    url(r'^goods_detail/', login_required(views.goods_detail), name='goods_detail'),
    # 商品信息修改
    url(r'^goods_detail_change/(?P<g_id>\d+)/', login_required(views.goods_detail_change), name='goods_detail_change'),
    # 商品删除1
    url(r'^goods_detail_delete/(?P<g_id>\d+)/', login_required(views.goods_detail_delete), name='goods_detail_delete'),
    # 商品删除2
    url(r'^goods_delete/(?P<g_id>\d+)/', login_required(views.goods_delete), name='goods_delete'),
    # 商品描述
    url(r'^goods_desc/(?P<g_id>\d+)/', login_required(views.goods_desc), name='goods_desc'),
]