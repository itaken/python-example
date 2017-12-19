#!/usr/bin/python3
# coding=utf8

import re
import time

from threading import Thread
# from multiprocessing import Process, cpu_count

import pymysql
import requests

# import sys
# reload(sys)
# sys.setdefaultencoding("utf8")

'''
获取 网页内容
'''
def grab_content(link):
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Kuaiso/1.42.501.445 Safari/537.36"
    }
    proxies = {
        'http': '111.56.5.41:80'  # 111.56.5.41:80
    }
    print("GET: " + link)
    if re.match('http', link) is None:  # 非链接
        return None
    
    try:
        res = requests.get(url=link, headers=headers, proxies=proxies, timeout=2)
    except:
        return None

    if res.status_code != 200:
        return None

    # print(res.headers['Content-Type']) # text/html
    if re.search('text/html', res.headers['Content-Type']) is None: 
        return None

    # print("GET: OK")

    return res.text #.encode('utf8');   # 内容

'''
解析页面的所有 URL
'''
def regex_urls(text):
    if text is None:
        return []

    match = re.findall('(src|href)="([^"]+)"', text)   # list

    urls = []
    for (_, link) in match:
        # url 判断
        if re.match('http', link) is None:
            continue
        
        if re.search('\.(css|jpg|gif|js|png|ico|mp4|mp3|flv|avi|jpeg|py)$', link) is not None:
            continue
        
        if len(link) > 150:
            continue

        urls.append(link)
    
    print("REGEX: OK")
    return urls

'''
URLs 入库
'''
def storage_urls(connection, links):
    if type(links) is not list:
        return 0

    params = []
    for link in links:
        timestamp = int(time.time())  # 时间戳
        params.append(('', link.encode('utf8'), timestamp, 0))

    cursor = connection.cursor()
    sql = "INSERT INTO `movie_demo_db`.`urls_tbl` (`title`, `url`, `add_time`, `is_view`) VALUES (%s, %s, %s, %s);"
    # sql  = sql % ('', 'url', 0, 0)
    cursor.executemany(sql, params)

    connection.commit()  # 提交
    # print(connection.insert_id())  # 获取最后插入ID
    # connection.close()  # 关闭连接
    # print(connection.affected_rows()) # 获取影响的行数
    affected_rows = connection.affected_rows()
    print("STORAGE: " + str(affected_rows))
    return affected_rows

'''
获取 链接
'''
def get_urls(connection, limit=100):
    cursor = connection.cursor()
    # 获取最旧 limit条数据
    sql = "SELECT `id`,`title`,`url`  FROM `movie_demo_db`.`urls_tbl` WHERE `is_view`=0 LIMIT 0," + str(limit) + ";"
    cursor.execute(sql)
    connection.commit()  
    links = []
    for row in cursor:
        links.append((row[0], row[2]))

    print("GET URLs: OK")
    return links


'''
更新 内容
'''
def update_storage(connection, id, title = ""):
    sql = "UPDATE `movie_demo_db`.`urls_tbl` SET `title` = %s, `is_view` = 1 WHERE `is_view` = 0 AND `id` = %s;"
    cursor = connection.cursor()
    # print(id)
    if type(id) == list:
        cursor.executemany(sql, id)
    else:
        id = int(id)
        if id < 1 or len(title) < 1:
            return 0

        # print(title.decode("utf8"))
        # exit(0)
        # print(type(title), title)
        cursor.execute(sql,(title, id))
    
    connection.commit()  # 提交
    
    affected_rows = connection.affected_rows()
    print("UPDATE: " + str(affected_rows))
    return affected_rows

'''
循环更新
'''
def loop_update(limit=100, thread_num=0):
    limit = int(limit)
    if limit < 1:
        return

    connection = pymysql.connect(host="localhost", port=3306, user="demo", password="demo", db="movie_demo_db", charset='utf8mb4')
    urls = get_urls(connection, limit)
    params = []
    for url_info in urls:
        id = url_info[0]
        url = url_info[1]
        content = grab_content(url)  # 抓取内容
        if content is None:
            params.append(("", id))
            continue

        res = re.search("<title>([^>]+)<\/title>", content)
        if res is None:
            params.append(("", id))
            continue
        
        title = res.groups(1)[0].strip()  # 获取标题
        if title == "" or len(title) < 1:
            params.append(("", id))
            continue

        content_urls = regex_urls(content)  # 匹配URLs
        storage_urls(connection, content_urls)  # URLs入库

        params.append((title, id))

    update_storage(connection, params)  # 更新库

    print("==Thread: ", thread_num)

    connection.close()


'''
线程循环
'''
def thread_loop(loop = 10):
    i=0
    td_list = []
    while i < loop:
        i += 1
        loop_update(100)
    #     td = Thread(target=loop_update, args=(100, i))
    #     td.start()
    #     td_list.append(td)
    
    # for td in td_list:
    #     td.join()

'''
主函数
'''
if __name__ == '__main__':
    # connection = pymysql.connect(host="localhost", port=3306, user="demo", password="demo", db="movie_demo_db", charset='utf8mb4')

    # url = "https://www.douban.com/"
    
    # content = grab_content(url)  # 抓取内容
    # urls = regex_urls(content)  # 匹配URLs
    # affected_rows = storage_urls(connection,urls)  # URLs入库

    # update_storage(connection, 1, "中文")
    
    thread_loop(10)

    
    # 多进程
    # pr_list = []
    # for i in range(cpu_count()):    
    #     pr = Process(target=thread_loop, args=(10, ))
    #     pr.start()
    #     pr_list.append(pr)

    # for pr in pr_list:
    #     pr.join()  

    # connection.close()
