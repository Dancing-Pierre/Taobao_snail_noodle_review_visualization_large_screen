# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: jieba_goods_and_comment_deal.py
# @Author: Yunchang,Wang
# @E-mail: 360812146@qq.com
# @Site: 
# @Time: 3月 01, 2023
# ---
from collections import Counter

import jieba
import pymysql


def get_comment_words():
    """
    获取评价中词组对应词频，写入MySQL
    :return:
    """
    # 新建comment_words表存储评价的分词及其次频率
    # comment_words表存在就删除掉
    cursor.execute("DROP TABLE IF EXISTS comment_words")
    sql = """ CREATE TABLE comment_words (
                      word VARCHAR(255) NOT NULL,
                      num INT(10) NOT NULL
                    );
                    """
    # 执行sql新建表
    cursor.execute(sql)
    # 搜索所有评论
    sql = "SELECT * FROM comments"
    cursor.execute(sql)
    result = cursor.fetchall()
    # 所有评价合并成一个大句子
    sentence = ''
    for i in result:
        comment = i[2]
        sentence = sentence + '。' + comment

    # 分词统计
    seg_list = jieba.cut(sentence)
    c = Counter()
    for x in seg_list:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1

    # most_common为统计结果列表，我们输出前一百个
    for j, (k, v) in zip(range(100), c.most_common(100)):
        print('%s  %d' % (k, v))
        # 写入数据库
        cursor.execute("insert into comment_words(word, num) values( %s, %s)", [k, v])
    conn.commit()


def get_goods_words():
    """
    获取商品介绍中词组对应词频，写入MySQL
    :return:
    """
    # 新建goods_words表存储评价的分词及其次频率
    # goods_words表存在就删除掉
    cursor.execute("DROP TABLE IF EXISTS goods_words")
    sql = """ CREATE TABLE goods_words (
                          word VARCHAR(255) NOT NULL,
                          num INT(10) NOT NULL
                        );
                        """
    # 执行sql新建表
    cursor.execute(sql)
    sql = "SELECT * FROM goods"
    cursor.execute(sql)
    result = cursor.fetchall()
    # 所有商品介绍合并成一个大句子
    sentence = ''
    for i in result:
        good = i[0]
        sentence = sentence + '。' + good

    # 分词统计
    seg_list = jieba.cut(sentence)
    c = Counter()
    for x in seg_list:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1

    # most_common为统计结果列表，我们输出前一百个
    for j, (k, v) in zip(range(100), c.most_common(100)):
        print('%s  %d' % (k, v))
        # 写入数据库
        cursor.execute("insert into goods_words(word, num) values( %s, %s)", [k, v])
    conn.commit()


if __name__ == '__main__':
    # 关闭日志,防止报出警告
    jieba.setLogLevel(jieba.logging.INFO)
    # 数据库链接
    conn = pymysql.connect(host="localhost",
                           port=3306,
                           user="root",
                           password="123456",
                           db="luosifen",
                           charset="utf8")
    cursor = conn.cursor()
    # 获取评论分词
    get_comment_words()
    print("=======================评论分词成功入库===============================")
    # 获取商品分词
    get_goods_words()
    print("=======================商品分词成功入库===============================")
    conn.close()
