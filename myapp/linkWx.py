import requests
import json


def access_token():
    """"
       获取access_token
    """
    APPID = 'wxbba728b000c444f5'
    APPSECRET = '4df975778fb87dbc76f8c0a11770b602'
    WECHAT_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + APPID + '&secret=' + APPSECRET
    response = requests.get(WECHAT_URL)
    result = response.json()
    return result["access_token"]


def databaseQuery(access_token, collection_name):
    """"
        检索数据库
       collection_name 集合的名称
       .limit() 括号内的数值限定返回的记录数
    """
    url = 'https://api.weixin.qq.com/tcb/databasequery?access_token=' + access_token
    data = {
        "env": "test1-6gus0twf20d7133b",
        "query": "db.collection(\"" + collection_name + "\").limit(100).get()"
    }
    response = requests.post(url, data=json.dumps(data))
    result = response.json()
    print(result)
    return result

access_token = access_token()
collection_name = 'place'
databaseQuery(access_token, collection_name)