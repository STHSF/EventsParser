#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: xueqiu.py
@time: 2018/10/30 2:31 PM
"""
import sys
sys.path.append("../")

from pyhanlp import *
from src.data_reader import read_full_data

news = read_full_data()
# print news['title']
# print news['content']

for index, item in news.iterrows():
    title, content = item['title'], item['content']
    title_list = HanLP.extractKeyword(title, 8)
    content_list = HanLP.extractSummary(content, 2)
    print(title, title_list)
    print(content, content_list)



# 新闻标题聚合

# 个股事件
# 新闻事件


# 关键词提取
# document = "水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，" \
#            "根据刚刚完成了水资源管理制度的考核，有部分省接近了红线的指标，" \
#            "有部分省超过红线的指标。对一些超过红线的地方，陈明忠表示，对一些取用水项目进行区域的限批，" \
#            "严格地进行水资源论证和取水许可的批准。"
# print(HanLP.extractKeyword(document, 8))


# 自动摘要
# print(HanLP.extractSummary(document, 3))


# 依存句法分析
# print(HanLP.parseDependency("徐先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。"))