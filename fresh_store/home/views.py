from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from goods.models import Goods, GoodsCategory
from users.models import User


def index(request):
    if request.method == 'GET':
        goods_dict = {}
        goods_type = []
        category_types = GoodsCategory.objects.all()
        category_types_list = GoodsCategory.CATEGORY_TYPE
        goods = Goods.objects.all()
        for type in category_types:
            for good in goods:
                if type.category_type == good.category_id:
                    if len(goods_type) < 4:
                        goods_type.append(good)
                goods_dict[type.category_type] = goods_type
            goods_type = []
        return render(request, 'index.html', {'goods_dict': goods_dict,
                                              'category_types_list': category_types_list,
                                              'category_types': category_types,
                                              })
    if request.method == 'POST':
        pass


def goods_list(request, g_type):
    if request.method == 'GET':
        page_number = int(request.GET.get('page', 1))
        goods = Goods.objects.filter(category_id=g_type)
        goods_new = goods.filter(is_new=True)
        paginator = Paginator(goods, 10)
        goods_page = paginator.page(page_number)
        category_types_list = GoodsCategory.CATEGORY_TYPE
        return render(request, 'list.html', {'goods': goods_page,
                                             'goods_new': goods_new,
                                             'category_types_list': category_types_list,
                                             'goods_type': int(g_type)})