import requests
import json


def getdistance(startlat, startlng, endlat, endlng):
    myAK = 'coOGuImd5yFgVszeG4Te5WErzIoGzP4D'  # 填写自己申请的AK
    head = r"https://api.map.baidu.com/routematrix/v2/driving?origins={},{}&destinations={},{}&ak={}"
    distanceurl = head.format(startlat, startlng, endlat, endlng, myAK)
    res = requests.get(distanceurl)
    dis_json_data = json.loads(res.text)
    if dis_json_data['status'] == 0:
        dic = dis_json_data["result"][0]
        distance = dic["distance"]["text"]
        time = dic["duration"]["text"]
        content = [distance, time]
    else:
        content = 0
    return content


if __name__ == '__main__':
    print(getdistance(40.45, 116.34, 40.34, 116.45))
