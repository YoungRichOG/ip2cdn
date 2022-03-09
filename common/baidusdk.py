#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy,json
from baidubce import bce_base_client
from baidubce.auth import bce_credentials
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce import bce_client_configuration

import configparser

config = configparser.ConfigParser()
config.read("conf.ini")

ak = config["baidu"]["ak"]
sk = config["baidu"]["sk"]

# 单个IP查询接口 Python示例代码
class ApiCenterClient(bce_base_client.BceBaseClient):

    def __init__(self, config=None):
        self.service_id = 'apiexplorer'
        self.region_supported = True
        self.config = copy.deepcopy(bce_client_configuration.DEFAULT_CONFIG)

        if config is not None:
            self.config.merge_non_none_values(config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)

    def demo(self,ip):
        path = b'/v2/utils'
        headers = {}
        headers[b'Content-Type'] = 'application/json;charset=UTF-8'

        params = {}

        params['action'] = 'describeIp'
        params['ip'] = ip

        body = ''
        return self._send_request(http_methods.GET, path, body, headers, params)

def main(ip):

    endpoint = 'http://cdn.baidubce.com'
    config = bce_client_configuration.BceClientConfiguration(credentials=bce_credentials.BceCredentials(ak, sk),
                                                             endpoint=endpoint)
    client = ApiCenterClient(config)

    try:
        res = client.demo(ip)
        cdn = json.loads((res.__dict__['raw_data']))['cdnIP']
        return ip + ',百度云CDN,' + str(cdn)

    except Exception as e:
        print(ip,e)