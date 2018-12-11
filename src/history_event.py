#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: history_event.py
@time: 2018/11/14 3:33 PM
将类簇转换成事件单元，并根据类簇中的节点id从文本中提取每个类簇对应的新闻，构成事件单元，然后提取每个事件单元涉及的股票。并且对每个事件单元提取关键词代表每个事件单元。所有的结果打包成pickle文件保存到本地。
"""
import pickle
from src.utills import event_util
from data_reader import import_news, import_title, get_event_news


# 导入通过singlepass聚类生成的类簇
path = "/Users/li/PycharmProjects/event_parser/src/"
clustering_path = path + 'model/clustering_new.pkl'
# with open(clustering_path, 'wb') as fw:
#     pickle.dump(clustering, fw)
clustering = pickle.load(open(clustering_path, 'rb'))
# clustering.print_result()

# 读取新闻文本
corpus_news = "/Users/li/PycharmProjects/event_parser/src/data/text_full_index.txt"
corpus_news_title = "/Users/li/PycharmProjects/event_parser/src/data/text_title_index.txt"
news_dict = import_news(corpus_news)
news_title_dict = import_title(corpus_news_title)

# 事件有效性判断
# effectiveness_events, non_effectiveness_events = event_util.events_effectiveness(clustering.cluster_list, news_dict)

event_unit_lists = []
# for cluster_index, cluster in enumerate(effectiveness_events):
for cluster_index, cluster in enumerate(clustering.cluster_list):
    print "cluster: %s" % cluster_index  # 簇的序号
    print cluster.node_list  # 该簇的节点列表

    event_unit = event_util.EventUnit()
    event_unit.node_list = cluster.node_list
    event_unit.node_num = cluster.node_num
    event_unit.centroid = cluster.centroid
    event_unit.event_id = cluster_index

    # 获取新闻标题
    event_title_lists = get_event_news(news_title_dict, cluster.node_list)
    # 获取新闻正文
    event_news_lists = get_event_news(news_dict, cluster.node_list)
    # 事件表示
    stock_lists, keywords_lists = event_util.event_expression(event_title_lists, event_news_lists)

    event_unit.stocks = stock_lists
    event_unit.keywords = keywords_lists
    event_unit_lists.append(event_unit)
    del event_unit
print "类簇的个数：%s" % len(clustering.cluster_list)
print "事件库中事件的个数 %s" % len(event_unit_lists)

# event_lib = EventLib()
# event_lib.event_unit_list = event_unit_lists

# # 保存事件库
path = "/Users/li/PycharmProjects/event_parser/src/"
event_unit_path = path + 'model/event_units_new.pkl'
with open(event_unit_path, 'wb') as fw:
    # pickle.dump(event_lib, fw)
    pickle.dump(event_unit_lists, fw)
