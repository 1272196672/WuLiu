from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from myapp.models import *
from pyecharts import options as opts
from pyecharts.charts import BMap
from pyecharts.commons.utils import JsCode
import requests
import time
import urllib.request
import gzip
import json


# Create your views here.


def manager_index(request):
    return render(request, 'myapp/index/manager_index.html')


def m_history(request):
    order_list = OrderMain.objects.filter(check_complete=1)
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
    return render(request, 'myapp/backstage/manager/m_history.html', content)


def m_monitor(request):
    order_list = OrderMain.objects.filter(check_complete=0)

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
    return render(request, 'myapp/backstage/manager/m_monitor.html', content)


def m_analyze_car(request):
    car = Car.objects.all()
    perSave = []
    for obj in car:
        save = 0
        unave = 0
        main = OrderMain.objects.filter(car_number=obj.car_number)
        for obj2 in main:
            if obj2.check_temperature == 0 and obj2.check_humidity == 0:
                save += 1
            else:
                unave += 1
        try:
            perSave.append(unave / (save + unave))
        except:
            print()
    content = {'mix_list': list(zip(car, perSave))}
    return render(request, 'myapp/backstage/manager/m_analyze_car.html', content)


def m_create_order(request, notification=""):
    goods = Commodity.objects.all()
    car = Car.objects.all()
    storehouse = Storage.objects.all()
    staff = Users.objects.all()
    content = {'goods_list': goods, 'car_list': car, 'storehouse_list': storehouse, 'staff_list': staff, 'notification': notification}
    return render(request, 'myapp/backstage/manager/m_create_order.html', content)


def m_create_order_op(request):
    order = OrderMain()
    timeOrder = OrderTime()
    # 需要传入实时温度数据，这里假设为11
    timeOrder.temperature = 11
    timeOrder.humidity = 11
    order.id = OrderMain.objects.all().last().id + 1
    order.commodity_id = request.GET['commodity_id']
    order.start_place = Storage.objects.filter(start_place=request.GET['start_place']).first()
    order.location = request.GET['end_place']
    # 计算时间消耗
    start_url = list(getUrl(str(order.start_place)[15:].strip("(").strip(")")))[0]
    end_url = list(getUrl(order.location))[0]
    print(start_url)
    print(end_url)
    start_lat, start_lng = getPosition(start_url)
    end_lat, end_lng = getPosition(end_url)
    lst = getdistance(start_lat, start_lng, end_lat, end_lng)
    print(lst)
    order.transportation_time = float(lst[1][:-2]) * 1.1
    # 计算结束时间
    lst1, lst2, lst3, lst4 = get_weather(get_weather_data(str(order.start_place)[16:-1]))
    if lst1 != '晴':
        if int(lst3) <= 2:
            order.end_time = time.strftime('%Y%m%d %H', time.localtime()) + "点+" + str(round(float(lst[1][:-2]) * 1.1, 1)) + 'h'
        elif int(lst3) <= 4:
            order.end_time = time.strftime('%Y%m%d %H', time.localtime()) + "点+" + str(
                round(float(lst[1][:-2]) * 1.1 * 1.04, 1)) + 'h'
        else:
            order.end_time = time.strftime('%Y%m%d %H', time.localtime()) + "点+" + str(
                round(float(lst[1][:-2]) * 1.1 * 1.1, 1)) + 'h'
    else:
        order.end_time = time.strftime('%Y%m%d %H', time.localtime()) + "点+" + lst[1][:-2] + 'h'
    if Commodity.objects.get(
            commodity_id=order.commodity_id).limit_temperature - 10 < timeOrder.temperature < Commodity.objects.get(
        commodity_id=order.commodity_id).limit_temperature - 10:
        order.check_temperature = 0
    else:
        order.check_temperature = 1
    if Commodity.objects.get(
            commodity_id=order.commodity_id).limit_humidity - 10 < timeOrder.humidity < Commodity.objects.get(
        commodity_id=order.commodity_id).limit_humidity - 10:
        order.check_humidity = 0
    else:
        order.check_humidity = 1
    order.car_number = Car.objects.filter(car_number=request.GET['car_number']).first()
    order.phone_number = request.GET['phone_number']
    order.check_complete = 0
    order.save()
    timeOrder.id = OrderMain.objects.filter(id=OrderMain.objects.all().last().id).first()
    timeOrder.realtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    timeOrder.probability_humidity = Commodity.objects.get(commodity_id=order.commodity_id).limit_humidity
    timeOrder.probability_temperature = Commodity.objects.get(commodity_id=order.commodity_id).limit_temperature
    timeOrder.save()
    return m_create_order(request, "订单创建成功!")


def m_goods(request):
    goods = Commodity.objects.all()
    content = {'goods_list': goods}
    return render(request, 'myapp/backstage/manager/m_goods.html', content)


def m_goods_add(request):
    return render(request, 'myapp/backstage/manager/m_goods_add.html')


def m_goods_add_op(request):
    goods = Commodity()
    goods.commodity_id = request.GET['goods_id']
    goods.commodity_name = request.GET['goods_name']
    goods.limit_temperature = request.GET['goods_temperature']
    goods.limit_humidity = request.GET['goods_humidity']
    goods.save()
    return m_goods(request)


def m_goods_modify(request, id=0):
    goods = Commodity.objects.get(commodity_id=id)
    content = {'goods': goods}
    return render(request, 'myapp/backstage/manager/m_goods_modify.html', content)


def m_goods_modify_op(request):
    goods = Commodity()
    goods.commodity_id = request.GET['goods_id']
    goods.commodity_name = request.GET['goods_name']
    goods.limit_temperature = request.GET['goods_temperature']
    goods.limit_humidity = request.GET['goods_humidity']
    goods.save()
    return m_goods(request)


def m_goods_del(request, id=0):
    goods = Commodity.objects.get(commodity_id=id)
    goods.delete()
    return m_goods(request)


def m_storehouse(request):
    storage = Storage.objects.all()
    storage_add = Storage()
    storage_add.start_place = request.GET.get('place')
    print(storage_add.start_place)
    if request.GET.get('place') is not None:
        storage_add.save()
    content = {'storage_list': storage}
    return render(request, 'myapp/backstage/manager/m_storehouse.html', content)


def m_warning(request):
    order_list = OrderMain.objects.all()
    order_list = order_list.filter(check_complete=0)
    id_list = []
    commodityId_list = []
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
        id_list.append(OrderTime.objects.get(id=obj.id))
        commodityId_list.append(Commodity.objects.get(commodity_id=obj.commodity_id))
    mix_list = list(zip(order_list, commodityId_list, id_list, warning_list))
    content = {'mix_list': mix_list}
    return render(request, 'myapp/backstage/manager/m_warning.html', content)


def m_warning_history(request):
    order_list = OrderMain.objects.all()
    order_list = order_list.filter(check_complete=1)
    id_list = []
    commodityId_list = []
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
        id_list.append(OrderTime.objects.get(id=obj.id))
        commodityId_list.append(Commodity.objects.get(commodity_id=obj.commodity_id))
    mix_list = list(zip(order_list, commodityId_list, id_list, warning_list))
    content = {'mix_list': mix_list}
    return render(request, 'myapp/backstage/manager/m_warning_history.html', content)


def getUrl(*address):
    '''
    调用地图API获取待查询地址专属url
    最高查询次数30w/天，最大并发量160/秒
    '''
    ak = 'wyysZdPfv503WDTI2nnuMyMsk6BGdrG9'
    if len(address) < 1:
        return None
    else:
        for add in address:
            url = 'http://api.map.baidu.com/geocoding/v3/?address={inputAddress}&output=json&ak={myAk}'.format(
                inputAddress=add, myAk=ak)
            yield url


def getPosition(url):
    '''返回经纬度信息'''
    res = requests.get(url)
    json_data = json.loads(res.text)

    if json_data['status'] == 0:
        lat = json_data['result']['location']['lat']  # 纬度
        lng = json_data['result']['location']['lng']  # 经度
    else:
        print("Error output!")
        return json_data['status']
    return lat, lng


def m_map(request, location):
    data = [
        [location, '你的位置']
    ]

    lat = 0
    lng = 0

    address = [location]
    for add in address:
        add_url = list(getUrl(add))[0]
        print(add_url)
        try:
            lat, lng = getPosition(add_url)
            print("运单地址：{0}|经度:{1}|纬度:{2}.".format(add, lng, lat))
        except:
            print('error')

    c = (
        BMap(init_opts=opts.InitOpts(width="1400px", height="800px"))
            # 百度地图开发应用 appkey，使用到百度地图的开发者自行到百度地图开发者中
            .add_schema(
            baidu_ak="wyysZdPfv503WDTI2nnuMyMsk6BGdrG9",
            center=[lng, lat],  # 当前视角的中心点，用经纬度表示
            zoom=16,  # 当前视角的缩放比例
            is_roam=True,  # 是否开启鼠标缩放和平移漫游
        )
            .add_coordinate(
            latitude=lat,
            longitude=lng,
            name=location,
        )
            .add(
            type_="effectScatter",  # 涟漪效果
            series_name="",  # 不使用的话会在地图上方有个小点
            data_pair=data,
            # data_pair = [list(z) for z in zip(['石家庄‘,'合肥','北京','上海','新疆'], [120,100,77,53,12])],
            # data_pair=[list(z) for z in zip(Faker.provinces, Faker.values())],  #生成虚假数据，方便调试
            symbol_size=5,
            effect_opts=opts.EffectOpts(),
            label_opts=opts.LabelOpts(
                position="top",  # 标签位置
                is_show=True,  # is_show是否显示标签,点上面的内容
                formatter=JsCode(  # formatter为标签内容格式器{a}：系列名;{b}：数据名;{c}：数值数组也可以是回调函数
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.value[2];
                    }
                }"""
                ),
                # 显示数据，可以去掉经纬度只显示数值return params.data.value[2] + ': ' + params.data.value[0]+': ' + params.data.value[1];
            ),
            itemstyle_opts=opts.ItemStyleOpts(),
            is_selected=True,  # 选中图例
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="物流",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#0C0C0C"),  # 文字样式配置
            ),
            tooltip_opts=opts.TooltipOpts(  # 标签配置，选中某一个点显示的框
                trigger="item",  # 触发类型，item主要用于散点图
                formatter=JsCode(  # 显示提示框formatter为标签内容格式器{a}：系列名;{b}：数据名;{c}：数值数组也可以是回调函数
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.name + '<br>' + params.data.value[2];
                    }
                }"""
                ),
                # 显示数据，可以去掉经纬度，只显示数值return params.data.value[2] + ': ' + params.data.value[0]+': ' + params.data.value[1];
            ),
        )
            .render(path="templates/myapp/map.html")
    )
    return render(request, 'myapp/map.html')


def getdistance(startlat, startlng, endlat, endlng):
    myAK = 'coOGuImd5yFgVszeG4Te5WErzIoGzP4D'  # 填写自己申请的AK
    head = r"https://api.map.baidu.com/routematrix/v2/driving?origins={},{}&destinations={},{}&ak={}"
    distanceurl = head.format(startlat, startlng, endlat, endlng, myAK)
    res = requests.get(distanceurl)
    dis_json_data = json.loads(res.text)
    print(distanceurl)
    print(dis_json_data)
    print(res)
    if dis_json_data['status'] == 0:
        dic = dis_json_data["result"][0]
        distance = dic["distance"]["text"]
        time = dic["duration"]["text"]
        content = [distance, time]
    else:
        content = 0
    return content


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
    return forecast[0].get('type'), forecast[1].get('type'), forecast[0].get('fengli')[9:-4], forecast[1].get('fengli')[9:-4]