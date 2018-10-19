from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from cart.models import ShoppingCart
from goods.models import Goods
from utils.CartAuthMiddleware import CartMiddleware


def add_cart(request):
    if request.method == 'POST':
        # 添加购物车数据，其实就是添加到session中
        # goods_dict = dict(request.POST)
        # if request.session.get('goods'):
        #     pass
        # else:
        #     request.session['goods'] = goods_dict
        good_id = request.POST.get('good_id')
        good_num = request.POST.get('good_num')
        good_list = [int(good_id), int(good_num), True]
        if request.session.get('goods'):
            flag = 0
            session_goods = request.session['goods']
            for goods in session_goods:
                if int(good_id) == goods[0]:
                    goods[1] = int(goods[1]) + int(good_num)
                    flag = 1
            if not flag:
                session_goods.append(good_list)
            request.session['goods'] = session_goods
            cart_count = len(session_goods)
        else:
            data = []
            data.append(good_list)
            request.session['goods'] = data
            cart_count = 1

        return JsonResponse({'code': 200, 'cart_count': cart_count})


def cart(request):
    if request.method == 'GET':
        try:
            goods = request.session.get('goods')
            if request.session.get('user_id'):
                request.session['goods'] = []
                goods = CartMiddleware.querydict_list(ShoppingCart.objects.filter(user_id=request.session.get('user_id')))
            goods_info = Goods.objects.filter(pk__in=[x[0] for x in goods])
            for good_info in goods_info:
                select_len = 0
                for good in goods:
                    if good[0] == good_info.id and len(good) == 3:
                        good.append(good_info.shop_price * good[1])
                    if good[2]:
                        select_len += 1

            return render(request, 'cart.html', {'goods': goods,
                                                 'goods_info': goods_info,
                                                 'len': len(goods),
                                                 'select_len': select_len})
        except:
            return render(request, 'cart.html', {'goods': [],
                                                 'goods_info': [],
                                                 'len': 0,
                                                 'select_len': 0})


def cart_updata(request):
    if request.method == 'GET':
        print('数据更新加载完成')


def cart_check_all(request):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        sum_price = 0
        count = 0
        if request.session.get('user_id'):
            goods = ShoppingCart.objects.filter(user_id=request.session.get('user_id'))
            if request.POST.get('all_use') == 'false':
                flag = 0
            else:
                flag = 1
                count = goods.__len__()
            for good in goods:
                if flag:
                    sum_price += good.nums * good.goods.shop_price
                good.is_select = bool(flag)
                good.save()
        else:
            session_goods = request.session.get('goods')
            goods_info = [[good.id, good.shop_price] for good in Goods.objects.all()]
            if request.POST.get('all_use') == 'false':
                flag = 0
            else:
                flag = 1
                count = len(session_goods)
            for session_good in session_goods:
                session_good[2] = bool(flag)
                if flag:
                    for good_info in goods_info:
                        if session_good[0] == good_info[0]:
                            price = good_info[1]
                    sum_price += session_good[1] * price
            request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'all': bool(flag), 'sum_price': sum_price, 'count': count})


def cart_check_one(request):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        sum_price = 0
        count = 0
        if request.session.get('user_id'):
            good = ShoppingCart.objects.filter(user_id=request.session.get('user_id'), goods_id=int(request.POST.get('one_id'))).first()
            if request.POST.get('one_use') == 'false':
                flag = 0
            else:
                flag = 1
            good.is_select = bool(flag)
            good.save()
            goods = ShoppingCart.objects.filter(user_id=request.session.get('user_id'))
            for good in goods:
                if good.is_select:
                    sum_price += good.nums * good.goods.shop_price
                    count += 1
        else:
            session_goods = request.session.get('goods')
            goods_info = [[good.id, good.shop_price] for good in Goods.objects.all()]
            if request.POST.get('one_use') == 'false':
                flag = 0
            else:
                flag = 1
            for session_good in session_goods:
                if session_good[0] == int(request.POST.get('one_id')):
                    session_good[2] = bool(flag)
            for session_good in session_goods:
                if session_good[2]:
                    for good_info in goods_info:
                        if good_info[0] == session_good[0]:
                            price = good_info[1]
                    sum_price += session_good[1] * price
                    count += 1
            request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'sum_price': sum_price, 'count': count})