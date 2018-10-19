from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from home.forms import UserLoginForm


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        pass


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # 验证成功
            user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home:index'))
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html', {'form': form})


def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponseRedirect(reverse('home:login'))
    if request.method == 'POST':
        pass






