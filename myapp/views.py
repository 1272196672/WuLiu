from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from myapp.models import *


# Create your views here.


def index(request):
    return render(request, 'myapp/index/index.html')


def login(request):
    return render(request, 'myapp/login_sign/login.html')


def login_control(request):
    career = request.POST.get('career', None)
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    content = {}
    if career == 'manager':
        if username == 'admin' and password == '123456':
            return HttpResponseRedirect(reverse('manager_index'))
        else:
            content['alert'] = '用户名或者密码错误'
            return render(request, 'myapp/login_sign/login.html', content)
    else:
        print(username, password)
        try:
            if Users.objects.get(username=username) and Users.objects.get(username=username).user_key == password:
                response = HttpResponseRedirect(reverse('staff_index'))
                response.set_cookie('username', username)
                return response
            else:
                content['alert'] = '用户名或者密码错误'
                return render(request, 'myapp/login_sign/login.html', content)
        except:
            content['alert'] = '用户名或者密码错误'
            return render(request, 'myapp/login_sign/login.html', content)


def sign(request):
    return render(request, 'myapp/login_sign/sign.html')


def sign_control(request):
    username = request.POST.get('account', None)
    password = request.POST.get('password', None)
    phone = request.POST.get('phone', None)
    rePassword = request.POST.get('rePassword', None)
    check = 1
    content = {}
    for obj in Users.objects.all():
        if obj.username == username or obj.phone_number == phone:
            check = 0
            break
    try:
        if password != rePassword:
            content['alert'] = '两次密码不相同'
            return render(request, 'myapp/login_sign/sign.html', content)
        if check == 0:
            content['alert'] = '存在相同账号或手机号已注册'
            return render(request, 'myapp/login_sign/sign.html', content)
        else:
            user = Users();
            user.user_key = password
            user.username = username
            user.phone_number = phone
            user.save()
            content['alert'] = '注册成功'
            return render(request, 'myapp/login_sign/sign.html', content)
    except:
        content['alert'] = '存在相同账号或手机号已注册'
        return render(request, 'myapp/login_sign/sign.html', content)


def coldchain(request):
    return render(request, 'myapp/introduction/coldchain.html')


def predict(request):
    return render(request, 'myapp/introduction/predict.html')
