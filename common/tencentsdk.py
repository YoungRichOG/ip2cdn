import json,time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cdn.v20180606 import cdn_client, models
import configparser

config = configparser.ConfigParser()
config.read("conf.ini")

ak = config["tencent"]["ak"]
sk = config["tencent"]["sk"]

def main(ip):
    time.sleep(1)
    try:
        cred = credential.Credential(ak, sk)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cdn.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cdn_client.CdnClient(cred, "", clientProfile)

        req = models.DescribeCdnIpRequest()
        params = {
            "Ips": [ip]
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeCdnIp(req)
        # print('tencent:',resp.to_json_string())

        _ip = json.loads(resp.to_json_string())['Ips'][0]['Ip']
        _cdn = json.loads(resp.to_json_string())['Ips'][0]['Platform']

        return _ip+',腾讯云CDN,'+_cdn

        # return resp.to_json_string()
    except TencentCloudSDKException as err:
        print(err)