#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: eventsUtill.py
@time: 2018/11/29 8:39 PM
事件表示，事件的有效性判断
"""
import numpy as np
from src.cluster.singlePass import singlePassCluster
from src.utills import tfidf


corpus_train = "/Users/li/PycharmProjects/event_parser/src/text_full_full.txt"


def events_list(news_title_list):
    for news in news_title_list:
        print news
    pass


def events_effectiveness(cluster_list, news_dict):
    """
    事件有效性判断
    :param cluster_list:
    :param news_dict:
    :return:
    """
    effectiveness_events = []
    non_effectiveness_events = []
    for cluster_index, cluster in enumerate(cluster_list):  # 遍历每一个事件类簇
        print "cluser: %s" % cluster_index  # 簇的序号
        print "node_list: %s" % cluster.node_list  # 该簇的节点列表
        centroid = cluster.centroid
        text_vectors_similary = []
        for node in cluster.node_list:  # 提取每个事件类簇中的结点，并且计算每个节点的文本向量空间
            # 获取结点对应的新闻
            news = news_dict.get(str(node))
            # 将新闻转换成文本向量空间
            text_vector = tfidf.load_tfidf_vectorizer([news]).toarray().reshape(-1)
            # 计算每篇文章与类簇中心的相似度
            similary = singlePassCluster.cosine_distance(text_vector, centroid)
            print "similary %s " % similary
            text_vectors_similary.append(similary)
        # 计算每个类簇中文章方差
        variance = np.var(text_vectors_similary)
        print "variance: %s" % variance

        # 如果方差大于某个阈值，则为无效事件
        if variance >= 12:
            non_effectiveness_events.append(cluster)
        else:
            effectiveness_events.append(cluster)

    print "length of effectiveness_events: %s" % len(effectiveness_events)
    print "length of non_effectiveness_events: %s" % len(effectiveness_events)
    return effectiveness_events, non_effectiveness_events


def event_expression(news_title_list, news_list):
    """
    事件表示，
    :return:
    """
    # 根据事件类簇中的新闻id，从原始
    for news in news_list:
        print news

    for news_title in news_title_list:
        print news_title


# 重复性事件合并


class eventLib(object):
    pass


def event_lib(event_list):
    pass


