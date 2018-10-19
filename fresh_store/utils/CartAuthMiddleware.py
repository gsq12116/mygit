from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart


class CartMiddleware(MiddlewareMixin):

    def process_request(self, request):
        cart_path = '/cart/cart_updata/'
        path = request.path
        if path != cart_path:
            return None
        else:
            if request.session.get('user_id'):
                db_news = ShoppingCart.objects.filter(user_id=request.session.get('user_id'))
                db_goods = self.querydict_list(db_news)
                session_goods = request.session.get('goods')
                if not session_goods:
                    session_goods = []
                for session_good in session_goods:
                    flag = 1
                    for db_good in db_goods[:]:
                        if int(session_good[0]) == db_good[0]:
                            flag = 0
                            session_good[1] = int(session_good[1])+int(db_good[1])
                            db_new = db_news.filter(goods_id=db_good[0]).first()
                            db_new.nums = session_good[1]
                            db_new.is_select = session_good[2]
                            db_new.save()
                            db_goods.remove(db_good)
                    if flag:
                        ShoppingCart.objects.create(user_id=request.session.get('user_id'),
                                                    goods_id=session_good[0],
                                                    nums=session_good[1],
                                                    is_select=session_good[2])
                try:
                    session_goods.extend(db_goods)
                except:
                    session_goods = []
                    session_goods.extend(db_goods)
                request.session['goods'] = session_goods
                return HttpResponseRedirect(reverse('cart:cart'))
            else:
                try:
                    request.session['goods']
                except:
                    request.session['goods'] = []
                return HttpResponseRedirect(reverse('cart:cart'))

    @staticmethod
    def querydict_list(querydict):
        query_list = []
        for x in querydict:
            q = [x.goods_id, x.nums, x.is_select]
            query_list.append(q)
        return query_list


