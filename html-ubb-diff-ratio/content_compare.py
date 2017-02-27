#!/usr/bin/python3
# 内容比对
# author: willike<regelhh@gmail.com>
# since : 2016-09-10
# license: MIT

import difflib   # 比对差异库
from content_match import ContentMatch


class ContentCompare(object):
    # 获取 UBB过滤详情
    @staticmethod
    def __get_ubb_filter_detail(goods_data, goods_id):
        if goods_data is None:
            return None

        if "detail" not in goods_data:
            print(str(goods_id) + " 解析UBB详情内容 失败")
            return None

        goods_detail = goods_data["detail"]  # UBB详情
        if goods_detail is None or goods_detail == "":
            return None

        filter_data = ContentMatch.ubb_filter(goods_detail)
        return filter_data

    # 获取 HTML过滤详情
    @staticmethod
    def __get_html_filter_detail(goods_data, goods_id):
        if goods_data is None:
            err_msg = str(goods_id) + " 没有相关数据"
            print(err_msg)
            return None

        if "detail" not in goods_data:  # 判断是否含有detail属性
            print(str(goods_id) + " 解析HTML详情内容 失败")
            return None

        goods_detail = goods_data["detail"]  # HTML详情
        if goods_detail is None or goods_detail == "":
            return None

        filter_data = ContentMatch.html_filter(goods_detail)
        return filter_data

    # ubb数据 和 html数据 的 比对
    @classmethod
    def ubb_and_html_diff_ratio(cls, ubb_data, html_data, goods_id):
        ubb_filter_data = cls.__get_ubb_filter_detail(ubb_data, goods_id)
        if ubb_filter_data is None:
            return None

        html_filter_data = cls.__get_html_filter_detail(html_data, goods_id)
        if html_filter_data is None:
            return None

        dif_sm = difflib.SequenceMatcher(None, ubb_filter_data, html_filter_data)
        dif_ratio = dif_sm.quick_ratio()  # 差异度
        # if dif_ratio < 0.9:
        #     print(goods_id, dif_ratio, ubb_filter_data, html_filter_data)
        #     quit()
        return round(dif_ratio, 3)  # 精度取两位

