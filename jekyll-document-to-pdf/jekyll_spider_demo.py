#!/usr/bin/python3
"""
    jekyll document spider demo

    @author willike
    @since 2017-02-18
    @description http://mp.weixin.qq.com/s/LH8nEFfVH4_tvYWo46CF5Q 阅读验证
"""
import requests
from bs4 import BeautifulSoup
import pdfkit

# jekyll 文档链接
document_url = "https://jekyllrb.com/docs/home/"

# html 模板
html_template = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        {content}
    </body>
</html>
"""

def parse_url_to_html(url):
    """
        获取链接文档内容并保存

        :param url: 文档链接
        :return:
    """
    response = requests.get(url)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find_all(class_="unit four-fifths")[0]  # 获取文档内容
    html = str(body)
    html = html_template.format(content=html)
    file_path = "./data/demo.html"
    with open(file_path, "wb") as f:
        f.write(bytes(html, "utf_8"))  # string转byte

    return file_path


def get_url_list(url):
    """
        获取链接列表

        :param url:
        :return:
    """
    response = requests.get(url)
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.content, "html5lib")
    aside_links = soup.find_all("aside")[1]  # 获取侧边栏内容
    urls = []
    for li in aside_links.find_all("li"):
        # 侧边栏 所有链接
        a_url = "https://jekyllrb.com/" + li.a.get("href")
        urls.append(a_url)

    return urls


def save_pdf(file_path):
    """
        把html文件保存成pdf文件

        :param file_path: html文件路径
        :return:
    """
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ]
    }
    pdfkit.from_file(file_path, "./data/demo.pdf", options=options)


# run demo
# file_name = parse_url_to_html(url=document_url)
# save_pdf(file_name=file_name)
