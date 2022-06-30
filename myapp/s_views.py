from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from myapp.models import *
import urllib.request
import gzip
import json

# Create your views here.


def staff_index(request):
    content = {}
    content['username'] = request.COOKIES.get('username')
    return render(request, 'myapp/index/staff_index.html', content)


def s_order_now(request):
    username = request.COOKIES['username']
    order_list = OrderMain.objects.filter(phone_number=(Users.objects.get(username=username).phone_number))
    order_list = order_list.filter(check_complete=0)

    weather_list = []
    warning_list = []
    tomorrow_list = []
    for obj in order_list:
        if obj.check_humidity == 1 and obj.check_temperature == 0:
            warning_list.append("湿度异常")
        elif obj.check_humidity == 0 and obj.check_temperature == 1:
            warning_list.append("温度异常")
        elif obj.check_humidity == 0 and obj.check_temperature == 0:
            warning_list.append("正常")
        else:
            warning_list.append("温度，湿度异常")
        lst1, lst2 = show_weather(get_weather_data(str(obj.start_place)[16:-1]))
        weather_list.append(lst1)
        tomorrow_list.append(lst2)
    id_list = []
    for obj in order_list:
        id_list.append(obj.id)
    th_list = OrderTime.objects.filter(id__in=id_list)
    mix_list = list(zip(order_list, th_list, warning_list, weather_list, tomorrow_list))
    content = {'mix_list': mix_list}
    return render(request, 'myapp/backstage/staff/s_order_now.html', content)


def s_order_history(request):
    username = request.COOKIES['username']
    order_list = OrderMain.objects.filter(phone_number=(Users.objects.get(username=username).phone_number))
    order_list = order_list.filter(check_complete=1)
    warning_list = []
    for obj in order_list:
        if obj.check_humidity == 1 and obj.check_temperature == 0:
            warning_list.append("湿度异常")
        elif obj.check_humidity == 0 and obj.check_temperature == 1:
            warning_list.append("温度异常")
        elif obj.check_humidity == 0 and obj.check_temperature == 0:
            warning_list.append("正常")
        else:
            warning_list.append("温度，湿度异常")
    id_list = []
    for obj in order_list:
        id_list.append(obj.id)
    th_list = OrderTime.objects.filter(id__in=id_list)
    mix_list = list(zip(order_list, th_list, warning_list))
    content = {'mix_list': mix_list}
    return render(request, 'myapp/backstage/staff/s_order_history.html', content)


def get_weather_data(city_name):
    url1 = 'http://wthrcdn.etouch.cn/weather_mini?city=' + urllib.parse.quote(city_name)
    # 网址1只需要输入城市名，网址2需要输入城市代码
    weather_data = urllib.request.urlopen(url1).read()
    # 读取网页数据
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    # 解压网页数据
    weather_dict = json.loads(weather_data)
    # 将json数据转换为dict数据
    return weather_dict


def show_weather(weather_data):
    weather_dict = weather_data
    forecast = []
    # 将json数据转换为dict数据
    if weather_dict.get('desc') == 'invilad-citykey':
        print('你输入的城市名有误，或者天气中心未收录你所在城市')
    elif weather_dict.get('desc') == 'OK':
        forecast = weather_dict.get('data').get('forecast')
    return forecast[0].get('high') + " " + forecast[0].get('low') + " " +  forecast[0].get(
        'type') + '天气' + " " + forecast[0].get('fengxiang') + forecast[0].get(
        'fengli')[9:-3], forecast[1].get('high') + " " +  forecast[1].get('low') + " " +  forecast[1].get(
        'type') + '天气' + " " + forecast[1].get('fengxiang') + forecast[1].get('fengli')[9:-3]


def get_weather(weather_data):
    weather_dict = weather_data
    forecast = []
    # 将json数据转换为dict数据
    if weather_dict.get('desc') == 'invilad-citykey':
        print('你输入的城市名有误，或者天气中心未收录你所在城市')
    elif weather_dict.get('desc') == 'OK':
        forecast = weather_dict.get('data').get('forecast')
    return forecast[0].get('type'), forecast[1].get('type')
