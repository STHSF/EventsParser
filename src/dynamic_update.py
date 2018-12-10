#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: dynamic_update.py
@time: 2018/12/5 2:23 PM
增量式事件更新，基于历史事件库，将新增新闻实时与历史事件库进行相似度计算，最后合并
"""
import time
from src.utills import event_util
from src.cluster.singlePass import singlePassCluster
from data_reader import get_ordered_data, trans_df_data


# 读取指定日期之后的新闻
# 读取当前时间段时间
now = int(time.time())
ordered_df = get_ordered_data(timestamp=now)
# 提取dataFrame中的内容
ordered_news_lists = trans_df_data(ordered_df)
for tmp in ordered_news_lists:
    print tmp[0], tmp[1]

# 导入历史事件
history_event_units = event_util.load_history_event()
print "[Info] 事件库中事件的个数 %s" % len(history_event_units)

# for index, event_unit in enumerate(history_event_units):
#     print "cluster: %s" % index  # 簇的序号
#     print event_unit.node_list  # 该簇的节点列表
#     print event_unit.centroid

len_news = len(ordered_news_lists)
new_event_units = []
new_event_units.extend(history_event_units)

min_cluster_index = 0
for news_index in range(len_news):  # 遍历每一篇新闻
    max_dist = singlePassCluster.cosine_distance(history_event_units[0].centroid, ordered_news_lists[news_index][2])
    for cluster_index, history_event_unit in enumerate(history_event_units[1:]):  # 遍历每一个事件单元
        # 计算当前新闻和每个事件元之间距离
        dist = singlePassCluster.cosine_distance(history_event_unit.centroid, ordered_news_lists[news_index][2])
        # print 'dist: %s' % dist
        # 找出最大的距离的事件元
        if dist > max_dist:
            max_dist = dist
            min_cluster_index = cluster_index + 1
    print '[Info] max_dist: %s' % max_dist
    print '[Info] min_cluster_index: %s' % min_cluster_index
    # 如果最大距离大于某一个阈值，则将该新闻归并到该事件单元
    if max_dist > 10:
        new_event_units[min_cluster_index].add_node(ordered_news_lists[news_index][0], ordered_news_lists[news_index][2])
    else:  # 否则则新建一个事件单元
        new_event = event_util.EventUnit()
        new_event.add_node(ordered_news_lists[news_index][0], ordered_news_lists[news_index])
        new_event_units.append(new_event)
        del new_event

print '[Info] 更新后的事件个数: %s' % len(new_event_units)

# # 将更新后的事件单元保存下来
save_name = '20181211'
save_path = "/Users/li/PycharmProjects/event_parser/src/model/event_model/"
# event_util.event_save(new_event_units, save_name, save_path)
event_util.event_load(save_path)