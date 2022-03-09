import requests,time
import datetime
from hashlib import sha256
from urllib import parse
import hmac
import base64
import configparser

config = configparser.ConfigParser()
config.read("conf.ini")

username = config["wangsu"]["username"]
apiKey = config["wangsu"]["apikey"]

post_url = 'https://open.chinanetcenter.com/api/tools/ip-info'


def getDate():
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    date_gmt = datetime.datetime.utcnow().strftime(GMT_FORMAT)
    return date_gmt

def getAuth(userName, apikey, date):
    signed_apikey = hmac.new(apikey.encode('utf-8'), date.encode('utf-8'), sha256).digest()
    signed_apikey = base64.b64encode(signed_apikey)
    signed_apikey = userName + ":" + signed_apikey.decode()
    signed_apikey = base64.b64encode(signed_apikey.encode('utf-8'))
    return signed_apikey

key = getAuth(username,apiKey,getDate())


def createHeader(authStr,date):
    headers = {
    'Date': date,
    'Accept': 'application/json',
    'Content-type': 'application/json',
    'Authorization': 'Basic ' + authStr.decode()
    }
    return headers


header = createHeader(key,getDate())

def main(ip):
    data = "{ip:['%s']}" %ip
    try:
        r = requests.post(url=post_url,headers=header,verify=False,data=data)

        return ip+',网宿云CDN,'+str(r.json()['result'][0]['isCdnIp'])
    except Exception as e:
        print('网宿云发生错误:',e)