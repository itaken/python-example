#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

# import urllib

# url = "http://www.zuzuche.com"
# html = urllib.urlopen(url=url)  # 获取内容
# content = html.read().decode('utf-8')
# print(content)

# import time
# from threading import Thread

# def sleeper(i):
#     print "thread %d sleeps for 5 seconds" % i
#     time.sleep(5)
#     print "thread %d woke up" % i

# for i in range(10):
#     t = Thread(target=sleeper, args=(i,))
#     t.start()

# # print(u'标题'.encode('utf8'))

# 获取cpu数
# from multiprocessing import cpu_count
# print(cpu_count())

# connection.commit()

# f = open(name="proxy.json", mode="r+")
# print(f.read())

# abc = 123
# def test(a):
#     abc = 789
#     print(abc, a)

# def test2(b):
#     print(abc, b)

# test(456)
# test2(678)

# if __name__ == '__main__':
#     print("当前线程是: %s" % threading.current_thread().name)
#     # 创建一个线程
#     td = threading.Thread(target=run_loop, name="LoopThread")
#     # 启动 刚创建的线程
#     td.start()
#     # 线程 等待 ( 等待子线程都执行完毕了,主线程再关闭 )
#     td.join()
#     print("线程 %s 结束." % threading.current_thread().name)

'''
python 页面截图
@see https://gist.github.com/rverton/d07a2232f4c0e1c2b9894e9bdb4fa6cf
WebDriver for Chrome https://sites.google.com/a/chromium.org/chromedriver/downloads
pip install selenium
'''
import os  

from optparse import OptionParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
CHROMEDRIVER_PATH = 'C:\chromedriver_win32\chromedriver.exe'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

def make_screenshot(url, output):
    # if not url.startswith('http'):
    #     raise Exception('URLs need to start with "http"')

    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH,
        chrome_options=chrome_options
    )  
    driver.get(url)
    driver.save_screenshot(output)
    driver.close()

if __name__ == '__main__':
    usage = "usage: %prog [options] <url> <output>"
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    print(options, args)
    
    if len(args) < 2:
        parser.error("please specify a URL and an output")

    make_screenshot(args[0], args[1])
