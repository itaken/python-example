#!/usr/bin/env python3
'''
抓取远程服务内容
author: willike<regelhh@gmail.com>
since : 2016-09-10
license: MIT
'''

import urllib.request
import hashlib
import time
import json


class ContentGrab(object):
    # 生成 post 数据
    @staticmethod
    def __generate_post_data(goods_id, is_web=False):
        goods_id = int(goods_id)
        if goods_id < 1:
            return None

        params = {
            "user_id": 0,
            "goods_id": goods_id
        }
        if is_web is True:
            params["platform"] = "web"  # 是否是web

        hash_str = (str(params) + "_api_test").replace(" ", "").replace("'", "\"").encode("utf-8")
        hash_code = hashlib.md5(hash_str).hexdigest()  # 校验码
        param_data = {
            "ctime": time.time(),  # 时间戳
            "api": "test_api",
            "sign": hash_code[8: -8],
            "params": params,
        }
        post_data = {
            "request": str(param_data)
        }
        return post_data

    # string 2 json
    @staticmethod
    def __goods_2_json(html_str, goods_id=0):
        if html_str is None or html_str == "":
            return None

        html_json = json.loads(html_str)  # JSON转译
        if html_json["result"] is not 200:
            print(goods_id, html_json["message"])
            return None

        if html_json["data"] == "" or html_json["data"] == []:
            err_msg = str(goods_id) + " 没有该服务内容"
            print(err_msg)
            return None

        goods_info = html_json["data"]
        return goods_info

    # 抓取 服务内容
    @classmethod
    def api_service_grab(cls, goods_id, is_web=False):
        post_data = cls.__generate_post_data(goods_id, is_web)
        if post_data is None:
            return None

        url = "http://xxx.xxx/sell_services.php"
        url = urllib.request.Request(url)  # 链接处理
        url.add_header("User-Agent", "TEST-api-urllib/0.1")  # 添加 UA
        # url.set_proxy("127.0.0.1:8080", "http")  # 设置代理
        data = urllib.parse.urlencode(post_data)  # POST数据处理
        data = data.encode("utf-8")
        try:
            html = urllib.request.urlopen(url=url, data=data)  # 获取内容
            html_str = html.read().decode('utf-8')
        except Exception as err:
            print("ERROR: ", err)
            return None

        # 数据返回错误
        if html_str is None or html_str == "":
            err_msg = str(goods_id) + " 没有返回数据"
            print(err_msg)
            return None

        return cls.__goods_2_json(html_str, goods_id)

