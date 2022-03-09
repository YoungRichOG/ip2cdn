# coding: utf-8

from huaweicloudsdkcore.auth.credentials import GlobalCredentials
from huaweicloudsdkcdn.v1.region.cdn_region import CdnRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcdn.v1 import *
import time
import configparser

config = configparser.ConfigParser()
config.read("conf.ini")

ak = config["huawei"]["ak"]
sk = config["huawei"]["sk"]

credentials = GlobalCredentials(ak, sk) \

client = CdnClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(CdnRegion.value_of("cn-north-1")) \
        .build()

request = ShowIpInfoRequest()

def main(ip):
    time.sleep(20)

    try:
        # request = ShowIpInfoRequest()
        request.ips = ip
        response = client.show_ip_info(request)
        return response
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)