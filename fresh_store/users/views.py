from datetime import timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from users.forms import UserForm, LoginForm
from users.models import User


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        login_info = LoginForm(request.POST)
        if login_info.is_valid():
            user = User.objects.filter(username=login_info.cleaned_data.get('username')).first()
            if user:
                if check_password(login_info.cleaned_data.get('password'), user.password):
                    request.session['user_id'] = user.id
                    out_time = timedelta(days=2)
                    request.session.set_expiry(out_time)
                    return HttpResponseRedirect(reverse('home:index'))
                else:
                    return render(request, 'login.html', {'error_p': '密码错误'})
            else:
                return render(request, 'login.html', {'error_u': '用户名错误'})
        else:
            return render(request, 'login.html', {'error_form': login_info})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        user_info = UserForm(request.POST)
        if user_info.is_valid():
            username = user_info.cleaned_data.get('username')
            password = make_password(user_info.cleaned_data.get('password'))
            mobile = user_info.cleaned_data.get('mobile')
            cpwd = request.POST.get('cpwd')
            email = request.POST.get('email')
            allow = request.POST.get('allow')
            if cpwd == user_info.cleaned_data.get('password'):
                if allow:
                    User.objects.create(username=username,
                                        password=password,
                                        mobile=mobile,
                                        email=email)
                    return HttpResponseRedirect(reverse('users:login'))
                else:
                    return render(request, 'register.html', {'error_allow': '请勾选同意”天天生鲜用户使用协议“'})
            else:
                return render(request, 'register.html', {'error_cpwd': '两次输入不相同'})
        else:
            return render(request, 'register.html', {'form': user_info.errors})


def logout(request):
    if request.method == 'GET':
        request.session.flush()
        request.user = None
        return HttpResponseRedirect(reverse('users:login'))
