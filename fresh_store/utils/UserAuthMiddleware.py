import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from users.models import User


class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.session.get('user_id'):
            user = User.objects.filter(id=request.session.get('user_id')).first()
            request.user = user
        path = request.path
        not_paths = ['/users/login/', '/users/register/', '/goods/detail/',
                     '/home/index/', '/cart/add_cart/', '/cart/cart/',
                     '/home/list/(.*)/', '/media/(.*)/', '/static/(.*)/',
                     '/cart/cart_updata/', '/cart/cart_check_all/', '/cart/cart_check_one/']
        if path == '/':
            return None
        for not_path in not_paths:
            if re.match(not_path, path):
                return None
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect(reverse('users:login'))




