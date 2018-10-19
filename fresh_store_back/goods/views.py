from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from goods.forms import GoodForm
from goods.models import GoodsCategory, Goods


def goods_category_list(request):
    if request.method == 'GET':
        categorys = GoodsCategory.objects.all()
        category_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_category_list.html', {'categorys': categorys,
                                                            'category_types': category_types})
    if request.method == 'POST':
        pass


def goods_category_detail(request, id):
    if request.method == 'GET':
        category = GoodsCategory.objects.filter(pk=id).first()
        category_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_category_detail.html',
                      {'category': category, 'category_types': category_types})
    if request.method == 'POST':
        category_front_image = request.FILES.get('category_front_image')
        if category_front_image:
            category = GoodsCategory.objects.filter(pk=id).first()
            category.category_front_image = category_front_image
            category.save()
        return HttpResponseRedirect(reverse('goods:goods_category_list'))


def goods_list(request):
    if request.method == 'GET':
        page_number = int(request.GET.get('page', 1))
        goods = Goods.objects.all()
        paginator = Paginator(goods, 8)
        goods_page = paginator.page(page_number)
        category_types = GoodsCategory.CATEGORY_TYPE
        return render(request, 'goods_list.html', {'goods': goods_page,
                                                   'category_types': category_types})
    if request.method == 'POST':
        pass


def goods_detail(request):
    category_types = GoodsCategory.CATEGORY_TYPE
    if request.method == 'GET':
        return render(request, 'goods_detail.html', {'category_types': category_types})
    if request.method == 'POST':
        form = GoodForm(request.POST)
        if form.is_valid():
            # 如果表单验证的字段名和数据库的字段名相同可以使用如下方式添加
            # data = form.cleaned_data
            # Goods.objects.create(**data)
            Goods.objects.create(name=form.cleaned_data.get('name'),
                                 goods_sn=form.cleaned_data.get('goods_sn'),
                                 goods_nums=request.POST.get('goods_nums'),
                                 market_price=request.POST.get('market_price'),
                                 shop_price=request.POST.get('shop_price'),
                                 goods_brief=form.cleaned_data.get('goods_brief'),
                                 category_id=form.cleaned_data.get('category'),
                                 goods_front_image=request.FILES.get('goods_front_image'))
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            return render(request, 'goods_detail.html', {'form': form, 'category_types': category_types})


def goods_detail_change(request, g_id):
    if request.method == 'GET':
        category_types = GoodsCategory.CATEGORY_TYPE
        good = Goods.objects.filter(pk=g_id).first()
        return render(request, 'goods_detail.html', {'good': good, 'category_types': category_types})
    if request.method == 'POST':
        good = Goods.objects.filter(pk=g_id).first()
        good.name = request.POST.get('name')
        good.goods_sn = request.POST.get('goods_sn')
        good.goods_nums = request.POST.get('goods_nums')
        good.market_price = request.POST.get('market_price')
        good.shop_price = request.POST.get('shop_price')
        good.goods_brief = request.POST.get('goods_brief')
        good.category_id = request.POST.get('category')
        if request.FILES.get('goods_front_image'):
            good.goods_front_image = request.FILES.get('goods_front_image')
        good.save()
        return HttpResponseRedirect(reverse('goods:goods_list'))


def goods_detail_delete(request, g_id):
    if request.method == 'GET':
        good = Goods.objects.filter(pk=g_id).first()
        good.delete()
        return HttpResponseRedirect(reverse('goods:goods_list'))
    if request.method == 'POST':
        pass


def goods_desc(request, g_id):
    if request.method == 'GET':
        good = Goods.objects.filter(pk=g_id).first()
        return render(request, 'goods_desc.html', {'good': good})
    if request.method == 'POST':
        good = Goods.objects.filter(pk=g_id).first()
        good.goods_desc = request.POST.get('content')
        good.save()
        return HttpResponseRedirect(reverse('goods:goods_list'))


def goods_delete(request, g_id):
    if request.method == 'POST':
        good = Goods.objects.filter(pk=g_id).first()
        good.delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})



