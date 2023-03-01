# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: visual_large_screen.py
# @Author: Yunchang,Wang
# @E-mail: 360812146@qq.com
# @Site: 
# @Time: 3月 01, 2023
# ---

import pandas as pd
import pymysql
from pyecharts import options as opts
from pyecharts.charts import *
from pyecharts.globals import ThemeType


def map_sales_areas():
    """
    销售商销售量
    """
    province_dict = {
        "北京": "北京市",
        "天津": "天津市",
        "河北": "河北省",
        "山西": "山西省",
        "内蒙古": "内蒙古自治区",
        "辽宁": "辽宁省",
        "吉林": "吉林省",
        "黑龙江": "黑龙江省",
        "上海": "上海市",
        "江苏": "江苏省",
        "浙江": "浙江省",
        "安徽": "安徽省",
        "福建": "福建省",
        "江西": "江西省",
        "山东": "山东省",
        "河南": "河南省",
        "湖北": "湖北省",
        "湖南": "湖南省",
        "广东": "广东省",
        "广西": "广西壮族自治区",
        "海南": "海南省",
        "重庆": "重庆市",
        "四川": "四川省",
        "贵州": "贵州省",
        "云南": "云南省",
        "西藏": "西藏自治区",
        "陕西": "陕西省",
        "甘肃": "甘肃省",
        "青海": "青海省",
        "宁夏": "宁夏回族自治区",
        "新疆": "新疆维吾尔自治区",
        "台湾": "台湾省",
        "香港": "香港特别行政区",
        "澳门": "澳门特别行政区",
        "新加坡": "新加坡",
        "美国": "美国",
        "澳大利亚": "澳大利亚"
    }
    sql = "SELECT * FROM goods"
    cursor.execute(sql)
    result = cursor.fetchall()
    areas = []
    area_list = []
    sales = []
    for i in result:
        areas.append(province_dict[i[4]])
        sales.append(i[3])
        if i[4] in area_list:
            pass
        else:
            area_list.append(province_dict[i[4]])
    sum_list = []
    # print(areas)
    print(area_list)
    # print(sales)
    # 循环计算各个地区的付款人数总和
    for k in area_list:
        sum = 0
        for i, j in zip(areas, sales):
            if i == k:
                sum += j
        sum_list.append(sum)
    print(sum_list)
    c = (
        Map(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
        .add("销售量", [list(z) for z in zip(area_list, sum_list)], "china", is_map_symbol_show=False,
             label_opts=opts.LabelOpts(is_show=False)
             )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="全国地区商家销售量", pos_left='center'),
            visualmap_opts=opts.VisualMapOpts(max_=max(sum_list)),
        )
        # .render("./html/china_map.html")
    )
    return c


def wordCloud():
    """
    搜索关键词的词频
    :return:
    """
    sql = "SELECT * FROM goods_words"
    cursor.execute(sql)
    # 元组
    result = cursor.fetchall()
    w = (
        WordCloud(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add(series_name="", data_pair=result, shape='circle', word_size_range=[15, 80])
        .set_global_opts(
            title_opts=opts.TitleOpts(title='搜索-关键词组', pos_left='center'),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
        # .render("./html/basic_wordcloud.html")
    )
    return w


def price_interval():
    """
    价格区间分布
    :return:
    """
    sql = "SELECT * FROM goods"
    cursor.execute(sql)
    # 元组
    result = cursor.fetchall()
    price = []
    for i in result:
        price.append(i[2])
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    x = ['价格区间：0~20', '价格区间：20~40', '价格区间：40~60', '价格区间：60~80', '价格区间：80~100', '价格区间：100以上']
    y = []
    for i in price:
        i = float(i)
        if 0 < i <= 20:
            a.append(1)
        if 20 < i <= 40:
            b.append(1)
        if 40 < i <= 60:
            c.append(1)
        if 60 < i <= 80:
            d.append(1)
        if 80 < i <= 100:
            e.append(1)
        if i > 100:
            f.append(1)
    for i in (a, b, c, d, e, f):
        y.append(len(i))

    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
        .add(
            "",
            [list(z) for z in zip(x, y)],
            radius=["30%", "75%"],
            center=["50%", "50%"],
            rosetype="area",
            label_opts=opts.LabelOpts(font_size=15, color='white', font_weight='bold')

        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title='价格区间分布', pos_left='center')
        )
        # .render('./html/rose_pie.html')
    )
    return c


def business_area_bar():
    """
    商家分布
    :return:
    """
    sql = "SELECT * FROM goods"
    cursor.execute(sql)
    result = cursor.fetchall()
    areas = []
    for i in result:
        areas.append(i[4])
    df = pd.DataFrame({'地区': areas})
    areas = df['地区']
    num_area = areas.value_counts()
    x = list(num_area.index)[0:10]
    y = list(num_area)[0:10]
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
        .add_xaxis(x)
        .add_yaxis("商家个数", y)
        .set_global_opts(
            title_opts=opts.TitleOpts(title='商家数量分布情况前十', pos_left='center'),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=15, color='white')),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=15))
        )
        .set_series_opts(label_opts=opts.LabelOpts(
            # 数据标签的颜色
            color='white', font_size=12
            # ,formatter #数据标签显示格式
        )  ##设置数据标签的格式s
        )
        # .render("./html/bar_business.html")
    )
    return c


def business_areaSales():
    """
    不同地区商家平均销售量
    :return:
    """
    sql = "SELECT * FROM goods"
    cursor.execute(sql)
    result = cursor.fetchall()
    areas = []
    area_list = []
    sales = []
    for i in result:
        areas.append(i[4])
        sales.append(i[3])
        if i[4] in area_list:
            pass
        else:
            area_list.append(i[4])
    sum_list = []
    # print(area_list)
    # 循环计算各个地区的付款人数总和
    for k in area_list:
        sum = 0
        for i, j in zip(areas, sales):
            if i == k:
                sum += j
        sum_list.append(sum)
    df = pd.DataFrame({'地区': areas})
    areas = df['地区']
    num_area = areas.value_counts()
    x = list(num_area.index)
    y = list(num_area)
    print(x, y)
    # 转换为字典
    commodity_list = dict(zip(x, y))
    sales_list = dict(zip(area_list, sum_list))
    tmp = []
    # 求出每个地区的商家平均销售数量
    for key in area_list:
        mean = sales_list[key] / commodity_list[key]
        tmp.append(int(mean))
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION))
        .add_xaxis(area_list)
        .add_yaxis("平均销售量", tmp)
        .set_global_opts(
            title_opts=opts.TitleOpts(title='不同地区商家的平均销售数量', pos_left='center'),
            legend_opts=opts.LegendOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=9, color='white')),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=10))
        )
        .set_series_opts(label_opts=opts.LabelOpts(color='white', is_show=True)  # 设置数据标签的格式s
                         )
        # .render("./html/areaSales_business.html")
    )
    return c


def Page_show():
    c = (
        Page(layout=Page.DraggablePageLayout)
        .add(
            map_sales_areas(),
            wordCloud(),
            # time_bar_commodity(),
            price_interval(),
            business_areaSales(),
            business_area_bar()
        )
        .render('./html/page.html')
    )


if __name__ == '__main__':
    # 数据库链接
    conn = pymysql.connect(host="localhost",
                           port=3306,
                           user="root",
                           password="123456",
                           db="luosifen",
                           charset="utf8")
    cursor = conn.cursor()
    # 把purchase_num字段为空的置0，不然下面varchar转int会报错
    cursor.execute("UPDATE goods SET purchase_num = 0 WHERE purchase_num = ''")
    # 提交修改
    conn.commit()
    # 因为purchase_num字段清洗完是varchar类型，转化为int方便后续计算
    cursor.execute("ALTER TABLE goods MODIFY purchase_num INT(32)")
    # 提交修改
    conn.commit()

    # 单独生成
    Page_show()
    # 可视化大屏
    Page.save_resize_html("./html/page.html", cfg_file="./html/chart_config.json", dest="./html/my_new_charts.html")
    conn.close()
