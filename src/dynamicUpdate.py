#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: dynamicUpdate.py
@time: 2018/12/5 2:23 PM
"""
import pickle


# 读取当前新闻
def load_news(timestamp):
    """
    根据时间戳读取实时新闻，对读取的新闻进行文本预处理，每篇文章生成
    :param timestamp:
    :return:
    """
    pass


# 导入历史事件
def load_history_event(event_path):
    """
    导入历史事件
    :param event_path:
    :return:
    """
    # 导入通过singlepass聚类生成的类簇
    path = "/Users/li/PycharmProjects/event_parser/src/data/"
    clustering_path = path + 'model/clustering.pkl'
    # with open(clustering_path, 'wb') as fw:
    #     pickle.dump(clustering, fw)
    clustering = pickle.load(open(clustering_path, 'rb'))
    # clustering.print_result()

    return clustering


