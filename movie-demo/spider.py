#!/usr/bin/python3
# -*- coding:UTF-8 -*-

import re
import requests
# import urllib.request 
import pymysql

import time

'''
The Python Standard Library https://docs.python.org/3/library/index.html

'''

url = "https://movie.douban.com/"

# http 头部
'''
List of User Agent Strings http://www.useragentstring.com/pages/useragentstring.php
List of User Agent strings https://deviceatlas.com/blog/list-of-user-agent-strings
UA list https://udger.com/resources/ua-list
'''
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
}

# 代理
'''
西刺免费代理IP http://www.xicidaili.com/
Anonymous/Distorting/Elite Proxy List http://proxydb.net/?anonlvl=2&anonlvl=3&anonlvl=4&response_time=30
码农很忙免费代理IP服务器 https://proxy.coderbusy.com/
http://www.python-requests.org/en/master/user/advanced/#proxies
'''

proxies = {
    'http': '111.56.5.41:80'
}

'''
urllib.request https://docs.python.org/3/library/urllib.request.html
Requests: HTTP for Humans http://www.python-requests.org/en/master/
'''
# urllib.request 与 requests

res = requests.get(url, headers=headers, proxies=proxies)

if res.status_code != 200:
    print(res)
    exit(0)

content = res.text #.encode('utf8');   # 内容


# 匹配内容
'''
https://docs.python.org/3/library/re.html
regular expressions https://regex101.com/
Regex Tester https://www.regexpal.com/
Rubular http://rubular.com/
'''

# findall 与 fullmatch
match = re.findall('(src|href)="([^"]+)"', content)   # lsit

urls = []
for (_, url) in match:
    # url 判断
    if re.match('http', url) is None:
        continue
    
    if re.search('\.(css|jpg|gif|js|png)$', url) is not None:
        continue

    urls.append(('', url, int(time.time()), 0))

# print(urls)

# 缓存 / 入库  
'''
REDIS缓存 https://pypi.python.org/pypi/redis
>>> import redis
>>> r = redis.StrictRedis(host='localhost', port=6379, db=0)
>>> r.set('foo', 'bar')
mysql
python2: MySQLdb  http://mysql-python.sourceforge.net/MySQLdb.html
python3:  https://pypi.python.org/pypi 查看包
官方,有点慢,不兼容MySQLdb https://pypi.python.org/pypi/mysql-connector-python  https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
PyMySQL,比mysql-connector-python快,可以与MySQLdb完全兼容 https://pypi.python.org/pypi/PyMySQL https://github.com/PyMySQL/PyMySQL
pip install pymysql
PyMySQL的Cython版本 https://github.com/nakagami/CyMySQL/
速度快, 基本与MySQLdb兼容 https://pypi.python.org/pypi/mysqlclient https://github.com/PyMySQL/mysqlclient-python
pip install mysqlclient

'''

connection = pymysql.connect(host="localhost", port=3306, user="demo", password="demo", db="movie_demo_db")
cursor = connection.cursor()
sql = "INSERT INTO `movie_demo_db`.`urls_tbl` (`title`, `url`, `add_time`, `is_view`) VALUES (%s, %s, %s, %s);"
# sql  = sql % ('', 'url', 123, 0)

cursor.executemany(sql, urls)


connection.commit()

# 协程

'''
Python 线程与协程  http://blog.rainy.im/2016/04/07/python-thread-and-coroutine/
Python 中的进程、线程、协程、同步、异步、回调 https://segmentfault.com/a/1190000001813992
'''




