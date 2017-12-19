#!/usr/bin/env python3
# coding=utf8

import urllib.request

urls = [
    # "http://proxydb.net/",
    "https://segmentfault.com/blogs"
]

for url in urls:
    # 获取内容
    req = urllib.request.Request(url)
    html = urllib.request.urlopen(req)
    content = html.read().decode("utf8")
    print(url, content)
