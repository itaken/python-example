#!/usr/bin/python3
"""
    jekyll document spider

    @author willike
    @since 2017-02-18
    @description 参考 https://github.com/lzjun567/crawler_html2pdf/blob/master/pdf/crawler.py
"""
import os.path
import requests
from bs4 import BeautifulSoup
import pdfkit
from urllib.parse import urlparse

# jekyll 文档链接
document_url = "https://jekyllrb.com/docs/home/"

# html 模板
html_template = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        {content}
    </body>
</html>
"""


def get_url_list(url):
    """
        获取链接列表

        :params url: 文档链接
        :return:
    """
    try:
        response = requests.get(url)
    except Exception:
        return []

    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.content, "html5lib")
    aside_links = soup.find_all("aside")[0]
    if aside_links == "":
        return []

    domain = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(url))
    urls = []
    for li in aside_links.find_all("li"):
        href_url = domain + li.a.get("href")  # 文档链接
        urls.append(href_url)

    return urls


def parse_url_to_html(url, file_path):
    """
        获取链接文档内容并保存

        :params url: 文档链接
        :params file_path: 保存文件的名称
        :return:
    """
    file_path = "./data/" + file_path
    if file_path is not None and os.path.exists(file_path):
        # 如果存在,则直接返回 路径
        return file_path

    try:
        response = requests.get(url)  # 获取URL内容
    except Exception:
        print("FAILD: " + url + " 抓取失败!")
        return

    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find_all(class_="unit four-fifths")[0]  # 解析正文
    try:
        soup.find(class_="improve right hide-on-mobiles").clear()  # 移除 improve
        soup.find(class_="section-nav").clear()  # 移除 底部导航
    except Exception as e:
        print("FAILD: " + url + " 处理失败!")
        pass

    html = html_template.format(content=body)
    # 保存文件
    with open(file_path, "wb") as f:
        f.write(bytes(html, "utf_8"))

    return file_path


def save_pdf(html_path, pdf_path):
    """
        html文件保存为pdf

        :params html_path: html文档路径
        :params pdf_path: pdf文档路径
        :return:
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'outline-depth': 10,
    }
    pdf_path = "./data/" + pdf_path
    try:
        pdfkit.from_file(html_path, pdf_path, options=options)
    except Exception:
        print("FAILD: " + pdf_path + " 生成失败!")
        return False
        pass

    print("SUCESS: " + pdf_path + " 生成完毕!")
    return True


def main():
    file_name = u"jekyll-document.pdf"
    urls = get_url_list(document_url)
    html_paths = [parse_url_to_html(url, str(index) + ".html") for index, url in enumerate(urls)]
    save_pdf(html_paths, file_name)


if __name__ == '__main__':
    main()
