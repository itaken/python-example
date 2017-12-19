#!/usr/bin/env python3
# 内容入库
# author: willike<regelhh@gmail.com>
# since : 2016-09-11
# license: MIT

import pymysql


class ContentStorage(object):
    # 连接对象
    conn = None

    # 构造函数
    def __init__(self):
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root",
            passwd="",
            db="goods_info_db",
            charset="utf8"
        )
        self.conn = conn

    # 写入数据库
    def content_to_db(self, storage_data):
        try:
            exec_sta = None
            conn = self.conn
            with conn.cursor() as cursor:
                goods_sql = """
                    INSERT INTO goods_info_tbl (`goods_id`,`user_id`,`ratio`,`title`,
                    `ubb_detail`,`html_detail`) VALUES (%s, %s, %s, %s, %s, %s);
                """
                exec_sta = cursor.execute(goods_sql, (
                    storage_data["goods_id"],
                    storage_data["user_id"],
                    storage_data["ratio"],
                    storage_data["title"],
                    storage_data["ubb_detail"],
                    storage_data["html_detail"]
                ))
            conn.commit()  # 手动提交
        except Exception as err:
            print("ERROR: ", err)
            pass
        # finally:
        #     conn.close()

        return exec_sta
