#!/usr/bin/python3
# 获取 User Agent
# @author willike<regelhh@gmail.com>
# @since 2016-09-12
# @license MIT

import urllib.request
import json
from bs4 import BeautifulSoup

ua_url = "http://www.useragentstring.com/pages/useragentstring.php?name=All"
default_ua = "Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)"

request = urllib.request.Request(ua_url)
request.add_header("User-Agent", default_ua)
request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
request.add_header("Referer", "https://www.google.com/")

try:
    response = urllib.request.urlopen(request)
    html = response.read()  # .decode("utf-8")
except Exception as err:
    print("ERROR: ", err)
    quit()

if html is None or html == "":
    print("HTML内容 获取失败")
    quit()

soup = BeautifulSoup(html, 'html.parser', from_encoding='UTF-8')
ul_nodes = soup.find_all("ul")
ua_list = []

for ul in ul_nodes:
    content = ul.li.a.get_text()
    if content is None or content == "":
        continue
    ua_list.append(content)

if ua_list is []:
    print("解析UA数据失败")
    quit()

# print(ua_list)
ua_list = json.dumps(ua_list)  # 转为JSON
f = open("UA.json", "w")
ua_str = str(ua_list)  # 转为string
f.write(ua_str)  # 写入文件
print("获取保存 UA 成功")
