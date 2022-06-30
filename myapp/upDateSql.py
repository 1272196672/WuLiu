import linkWx
from myapp.models import *

def updateOrderMain():
    access_token = linkWx.access_token()
    data = linkWx.databaseQuery(access_token, "orderMain")
    orderMain = OrderMain()
    orderMain = OrderMain(id=data.id, commodity_id=data.commodity_id, start_place=data.start_place, location=data.location, end_time=data.end_time, transportation_time=data.transportation_time)
    orderMain.save()


def updateOrderTime():
    access_token = linkWx.access_token()
    data = linkWx.databaseQuery(access_token, "orderTime")
    orderTime = OrderTime()
    orderTime = OrderTime(id=data.id, realtime=data.realtime, temperature=data.temperature, humidity=data.humidity, probability_temperature=data.probability_temperature, probability_humidity=data.probability_humidity)
    orderTime.save()