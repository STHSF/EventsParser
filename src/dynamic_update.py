#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: dynamic_update.py
@time: 2018/12/5 2:23 PM
"""
import time
from src.utills import event_util
from data_reader import get_ordered_data, trans_df_data


# 读取指定日期之后的新闻
now = int(time.time())
ordered_df = get_ordered_data(timestamp=now)
print ordered_df
# 提取dataframe中的内容
ordered_news_lists = trans_df_data(ordered_df)


# 导入历史事件
history_event_units = event_util.load_history_event()

print "事件库中事件的个数 %s" % len(history_event_units)

for index, event_unit in enumerate(history_event_units):
    print "cluster: %s" % index  # 簇的序号
    print event_unit.node_list  # 该簇的节点列表
    print event_unit.centroid
