# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: data_cleaning.py
# @Author: Yunchang,Wang
# @E-mail: 360812146@qq.com
# @Site: 
# @Time: 3月 01, 2023
# ---
import re

import pymysql


def goods_address_data_update():
    """
    商品发货地数据清洗，忽略市级城市，保留省级地名
    """
    sql = "SELECT * FROM goods"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        local = i[4]
        # 如果有空格证明有市级城市
        if ' ' in local:
            local = ''.join(re.findall(r"(.*) ", local))
        print(local)
        # 执行更新语句
        query = f"UPDATE goods SET location = '{local}' WHERE goods_name  = '{i[0]}'"
        cursor.execute(query)
        conn.commit()


def number_of_payers_update():
    """
    付款人数清洗，1.5万+人付款 ---->  15000
    """
    sql = "SELECT * FROM goods"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        num = i[3]
        # 如果有万直接正则后乘10000
        if '万' in num:
            num = ''.join(re.findall(r"\d+\.?\d*", num))
            num = float(num) * 10000
        else:
            num = ''.join(re.findall(r"\d+\.?\d*", num))
        print(num)
        # 执行更新语句
        query = f"UPDATE goods SET purchase_num = '{num}' WHERE goods_name  = '{i[0]}'"
        cursor.execute(query)
        conn.commit()


if __name__ == "__main__":
    # 数据库链接
    conn = pymysql.connect(host="localhost",
                           port=3306,
                           user="root",
                           password="123456",
                           db="luosifen",
                           charset="utf8")
    cursor = conn.cursor()
    # 商品发货地数据清洗，忽略市级城市，保留省级地名
    # goods_address_data_update()
    # 付款人数清洗，1.5万+人付款 ---->  15000
    number_of_payers_update()
