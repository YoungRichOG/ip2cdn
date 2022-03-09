#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkcdn.request.v20180510.DescribeIpInfoRequest import DescribeIpInfoRequest
import time,json
import configparser

config = configparser.ConfigParser()
config.read("conf.ini")

ak = config["ali"]["ak"]
sk = config["ali"]["sk"]

credentials = AccessKeyCredential(ak, sk)

client = AcsClient(credential=credentials)

request = DescribeIpInfoRequest()
request.set_accept_format('json')

def main(ip):
    time.sleep(2)
    request.set_IP(ip)

    try:
        response = client.do_action_with_exception(request)
        data = json.loads(response.decode())
        return ip+',阿里云CDN,'+data['CdnIp']
    except:
        return ip + ',阿里云CDN,请求过快'