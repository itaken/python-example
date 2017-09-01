#!/usr/bin/python3
# 正则替换内容
# author: willike<regelhh@gmail.com>
# since : 2016-09-10
# license: MIT

import re


class ContentMatch(object):
    # 匹配
    @staticmethod
    def __mrpl(match):
        match_list = re.findall(r'src="([^"]+)"', match.group(0))  # 匹配所有
        if match_list is not None:
            # 返回list,组装成string
            return ''.join(match_list)

        return match.group(1)

    # HTML标签 过滤
    @classmethod
    def html_filter(cls, html_str):
        reg = re.compile('<img [^/]*src="([^"]+)"[^/]*/>', re.IGNORECASE)
        html_rpl = reg.subn(cls.__mrpl, html_str)  # 正则 函数替换
        tag_reg = re.compile('<[^>]+>|\s+|&#\d+|&[a-z]+;')
        match = tag_reg.sub('', html_rpl[0])
        return match

    # UBB标签 过滤
    @classmethod
    def ubb_filter(cls, ubb_str):
        reg = re.compile('\[[^\]]+\]|\s+|&#\d+|&[a-z]+;')
        match = reg.sub('', ubb_str)  # 正则替换
        return match

