from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from goods.models import Goods


def detail(request, g_id):
    if request.method == 'GET':
        good = Goods.objects.filter(pk=g_id).first()
        return render(request, 'detail.html', {'good': good})



