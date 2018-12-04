#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: mainProcess.py
@time: 2018/11/14 3:33 PM
"""
import pickle
from utills import eventsUtill


def import_title(corpus_path):
    """
    将新闻的news_id和新闻的标题news_title转换成dict，为后面从类簇中提取节点对应的新闻标题使用
    :param corpus_path: 语料的路径
    :return: dict, {news_id: news_title}
    """
    title_text_dict = {}
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 3:
            category = line[0]
            title = line[2]
            title_text_dict[category] = title
    return title_text_dict


def import_news(corpus_path):

    """
    将新闻的news_id和新闻的标题news_title转换成dict，为后面从类簇中提取节点对应的新闻标题使用
    :param corpus_path: 语料的路径
    :return: dict, {news_id: news_title}
    """
    news_dict = {}
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 3:
            news_id = line[0]
            word_list = line[2]
            news_dict[news_id] = word_list
    return news_dict


def get_event_news(text_dict, node_list):
    """
    从text_dict中提取node_list里面所有的对应的新闻或者新闻标题内容
    :param text_dict:dict: {news_id: news_title+content}
    :param node_list: list: [news_id]
    :return: list: [news_title+content]
    """
    # 读取文章中的内容
    text_list = []
    for node in node_list:
        text_list.append(text_dict.get(str(node)))

    return text_list


# 导入通过singlepass聚类生成的类簇
path = "/Users/li/PycharmProjects/event_parser/src/"
clustering_path = path + 'model/clustering.pkl'
# with open(clustering_path, 'wb') as fw:
#     pickle.dump(clustering, fw)
clustering = pickle.load(open(clustering_path, 'rb'))
# clustering.print_result()

# 读取新闻文本
corpus_news = "/Users/li/PycharmProjects/event_parser/src/text_full_full.txt"
corpus_news_title = "/Users/li/PycharmProjects/event_parser/src/text_title.txt"
news_dict = import_news(corpus_news)
news_title_dict = import_title(corpus_news_title)

# eventsUtill.events_effectiveness(clustering.cluster_list, news_dict)
#
for cluster_index, cluster in enumerate(clustering.cluster_list):
    print "cluster: %s" % cluster_index  # 簇的序号
    print cluster.node_list  # 该簇的节点列表

    # 获取新闻标题
    event_title_lists = get_event_news(news_title_dict, cluster.node_list)
    # 获取新闻正文
    event_news_lists = get_event_news(news_dict, cluster.node_list)
    eventsUtill.event_expression(event_title_lists, event_news_lists)






