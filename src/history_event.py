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
from src.configure import conf
from src.utils import event_util, tfidf
from data_reader import import_news, import_title, get_event_news


# 导入通过singlepass聚类生成的类簇
# clustering_path = '/Users/li/PycharmProjects/event_parser/src/model/clustering_new.pkl'
clustering_path = conf.clustering_save_path
# with open(clustering_path, 'wb') as fw:
#     pickle.dump(clustering, fw)
clustering = pickle.load(open(clustering_path, 'rb'))
# clustering.print_result()

# 读取新闻文本
# 新闻保存的路径
# corpus_news = "/Users/li/PycharmProjects/event_parser/src/data/text_full_index.txt"
corpus_news = conf.corpus_news
# 新闻标题保存的路径
# corpus_news_title = "/Users/li/PycharmProjects/event_parser/src/data/text_title_index.txt"
corpus_news_title = conf.corpus_news_title
# 构建新闻正文词典
news_dict = import_news(corpus_news)
# 构建新闻标题词典
news_title_dict = import_title(corpus_news_title)
# 事件有效性判断
# effectiveness_events, non_effectiveness_events = event_util.events_effectiveness(clustering.cluster_list, news_dict)

'''
构建事件单元
'''
event_unit_lists = []
# for cluster_index, cluster in enumerate(effectiveness_events):
for cluster_index, cluster in enumerate(clustering.cluster_list):
    print "[event_id]:%s " % cluster_index  # 簇的序号
    print "[event_node_id]: %s " % cluster.node_list  # 该簇的节点列表

    event_unit = event_util.EventUnit()
    event_unit.node_list = cluster.node_list
    event_unit.node_num = cluster.node_num
    event_unit.centroid = cluster.centroid
    event_unit.event_id = cluster_index

    # 获取事件单元中的标题
    event_title_lists = get_event_news(news_title_dict, cluster.node_list)
    # 获取事件单元中的新闻正文
    event_news_lists = get_event_news(news_dict, cluster.node_list)
    # # 事件表示,提取事件中涉及的股票，对所有新闻提取关键词, 添加事件标题
    # stock_list, keywords_list = event_util.event_expression(event_title_lists, event_news_lists)
    # # 事件表示， 计算事件的标题
    # topic_title = event_util.units_title(cluster, news_dict, news_title_dict)
    # print "[事件标题]:\n %s " % topic_title
    # event_unit.topic_title, event_unit.stocks, event_unit.keywords = topic_title, stock_list, keywords_list

    # 添加涉及的股票和事件关键词
    event_unit.event_expression(event_title_lists, event_news_lists)
    # 添加事件标题
    event_unit.add_units_title(news_dict, news_title_dict)
    event_unit_lists.append(event_unit)
    del event_unit
print "[类簇的个数]: %s" % len(clustering.cluster_list)
print "[事件库中事件的个数]: %s" % len(event_unit_lists)

# event_lib = EventLib()
# event_lib.event_unit_list = event_unit_lists

# # 保存事件库
# # event_unit_path = '/Users/li/PycharmProjects/event_parser/src/model/event_units_new.pkl'
# event_unit_path = conf.event_unit_path
# with open(event_unit_path, 'wb') as fw:
#     # pickle.dump(event_lib, fw)
#     pickle.dump(event_unit_lists, fw)
