from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,
                                 password=password)
        if user:
            auth.login(request, user)
            return JsonResponse({'code': 200})
        else:
            return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('home:login'))