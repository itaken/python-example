#!/usr/bin/python3
# UBB内容校验
# author: willike<regelhh@gmail.com>
# since : 2016-09-10
# license: MIT

from content_grab import ContentGrab
from content_compare import ContentCompare
from content_storage import ContentStorage


# 获取匹配度
def content_diff_ration(goods_id):
    goods_data = ContentGrab.api_service_grab(goods_id, False)
    if goods_data is None:
        return None

    web_goods_data = ContentGrab.api_service_grab(goods_id, True)
    if web_goods_data is None:
        return None

    diff_ratio = ContentCompare.ubb_and_html_diff_ratio(goods_data, web_goods_data, goods_id)

    if diff_ratio is not None:
        # 数据入库
        storage_data = {
            "goods_id": goods_id,
            "user_id": goods_data["user_id"],
            "title": goods_data["title"],
            "ubb_detail": goods_data["detail"],
            "html_detail": web_goods_data["detail"],
            "ratio": diff_ratio
        }
        ContentStorage().content_to_db(storage_data)

    return diff_ratio


if __name__ == '__main__':
    print("UBB校验开始: ")
    try:
        goods_id = 210000
        rg_list = range(0, 10000)  # 循环次数
        for i in rg_list:
            goods_id += 1
            ratio = content_diff_ration(goods_id)

            if ratio is None:
                err_msg = str(goods_id) + " 没有匹配值"
                print(err_msg)
                continue

            rd_msg = str(goods_id) + " UBB匹配度: " + str(ratio)
            print(rd_msg)
    except KeyboardInterrupt:  # 键盘退出
        print("BeyBye~")
        quit()

    print("检查完毕!")


