#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: event_util.py
@time: 2018/11/29 8:39 PM
事件表示，事件的有效性判断
"""

import os
import time
import pickle
import datetime
import numpy as np
from src.configure import conf
from src.cluster.singlePass import singlePassCluster
from src.cluster.singlePass.singlePassCluster import ClusterUnit
from src.utils import tfidf, data_process, dicts, keywords_extractor

# corpus_train = "/Users/li/PycharmProjects/event_parser/src/text_full_index.txt"
corpus_train = conf.corpus_train_path

data_process = data_process.DataPressing()


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
        print "[cluster]: %s" % cluster_index  # 簇的序号
        print "[node_list]: %s" % cluster.node_list  # 该簇的节点列表
        centroid = cluster.centroid
        text_vectors_similarly = []
        for node in cluster.node_list:  # 提取每个事件类簇中的结点，并且计算每个节点的文本向量空间
            # 获取结点对应的新闻
            news = news_dict.get(str(node))
            # 将新闻转换成文本向量空间
            text_vector = tfidf.load_tfidf_vectorizer([news]).toarray().reshape(-1)
            # 计算每篇文章与类簇中心的相似度
            similarly = singlePassCluster.cosine_distance(text_vector, centroid)
            print "[similarly] %s " % similarly
            text_vectors_similarly.append(similarly)
        # 计算每个类簇中文章方差
        variance = np.var(text_vectors_similarly)
        print "[variance]: %s" % variance

        # 如果方差大于某个阈值，则为无效事件
        if variance >= 10000:
            non_effectiveness_events.append(cluster)
        else:
            effectiveness_events.append(cluster)

    print "[length of effectiveness_events]: %s" % len(effectiveness_events)
    print "[length of non_effectiveness_events]: %s" % len(effectiveness_events)
    return effectiveness_events, non_effectiveness_events


def event_expression(news_title_list, news_list):
    """
    事件表示，
    :return:
    """
    # 根据事件类簇中的新闻id，从原始
    stock_lists = []
    news_lists = []
    for news in news_list:
        # print news
        # 提取正文中提及到的股票代码
        content_list = news.split(" ")
        stock_list = data_process.find_stocks(content_list=content_list, stock_dicts=dicts.stock_dict)
        stock_lists.extend(stock_list)
        news_lists.extend(content_list)
    # 事件中涉及的股票
    stocks = ",".join(item for item in set(stock_lists))
    print "[事件中包含的股票]: %s " % stocks

    # 事件簇关健词提取
    event_new_string = ' '.join(item for item in news_lists)
    # print "事件类簇 %s" % event_new_string
    event_keywords_list = keywords_extractor.parallel_test(news_lists)
    event_keywords = ','.join(item for item in event_keywords_list)
    print "[事件关键词]:\n %s " % event_keywords

    # 事件表示,事件要素抽取
    # 事件包含的新闻正文
    print '[事件包含的新闻正文]:'
    for news in news_list:
        print news

    # 事件包含的新闻标题
    print '[事件包含的新闻标题]:'
    for news_title in news_title_list:
        print news_title
    return stock_lists, event_keywords


def units_title(cluster, news_dict, news_title_dict):
    """
    提取事件单元的标题，
    :param cluster:
    :param news_dict:
    :param news_title_dict:
    :return:
    """
    node_list = cluster.node_list

    distance_list = []
    # print 'first node: %s' % node_list[0]
    # 事件单元中第一节点的td-idf
    node0_tf_idf = tfidf.load_tfidf_vectorizer([news_dict[node_list[0]]]).toarray().reshape(-1)
    max_dist = singlePassCluster.cosine_distance(cluster.centroid, node0_tf_idf)
    distance_list.append(max_dist)
    topic_node = node_list[0]
    for node_index, node in enumerate(node_list[1:]):
        # print 'event node: %s' % node
        # 计算每个节点的空间向量
        node_tf_idf = tfidf.load_tfidf_vectorizer([news_dict[node]]).toarray().reshape(-1)
        # 计算每个节点到簇心的欧式距离
        temp_dist = singlePassCluster.cosine_distance(cluster.centroid, node_tf_idf)
        distance_list.append(temp_dist)
        # 读取相似度最大的节点
        if temp_dist >= max_dist:
            max_dist = temp_dist
            topic_node = node
    # print "distance_list: %s" % distance_list
    # print "max_distance: %s" % max_dist
    # print "topic_node: %s" % topic_node
    # 返回相似度最大的节点对应的新闻标题
    return news_title_dict[topic_node]


def load_history_event(event_unit_path=None):
    """
    导入历史事件单元库
    :param event_unit_path:
    :return:
    """
    if event_unit_path is None:
        # event_unit_path = '/Users/li/PycharmProjects/event_parser/src/model/event_units_new.pkl'
        event_unit_path = conf.event_unit_path
    print '[读取的事件文件目录]: %s' % event_unit_path
    event_unit_lists = pickle.load(open(event_unit_path, 'rb'))

    # print "事件库中事件的个数 %s" % len(event_unit_lists)
    # for index, event_unit in enumerate(event_unit_lists):
    #     print "cluster: %s" % index  # 簇的序号
    #     print event_unit.node_list  # 该簇的节点列表
    #     print event_unit.centroid

    return event_unit_lists


def event_save(event_units, save_name=None, save_path=None):
    if save_name is None:
        save_name = str(int(time.time()))
    if save_path is None:
        save_path = "../event_model/"
        print("[event_util Info]当前文件夹: %s" % save_path)
    clustering_path = save_path + '%s.pkl' % save_name
    with open(clustering_path, 'wb') as fw:
        pickle.dump(event_units, fw)


def event_load(save_path):
    """
    从文件夹中读取最新的事件单元保存文件。
    :param save_path: 目录地址
    :return:
    """
    lists = os.listdir(save_path)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(save_path + fn))  # 将文件按时间排序
    filetime = datetime.datetime.fromtimestamp(os.path.getmtime(save_path+lists[-1]))
    file_new = os.path.join(save_path, lists[-1])  # 获取最新的文件保存到file_new
    print("[event_util Info] 时间：" + filetime.strftime('%Y-%m-%d %H-%M-%S'))
    print("[event_util Info] 最新修改的文件(夹)：" + lists[-1])
    return file_new


# 重复性事件合并? 可以手动标记然后合并

class EventUnit(singlePassCluster.ClusterUnit):
    """
    定义一个事件单元
    """
    def __init__(self):
        ClusterUnit.__init__(self)
        self.event_id = ''
        self.topic_title = " "
        self.start_time = ''  # 起始时间
        self.stop_time = ''   # 截止时间
        self.keywords = []
        self.stocks = []
        self.event_tag = 0  # 判断时间是否为新事件, 0为旧事件, 1为新事件. 如果是新事件, 则进行标题等的更新.

    def add_node(self, node, node_vec):
        ClusterUnit.add_node(self, node, node_vec)
        self.event_tag = 1  # 添加了新的节点，将该事件标记为更新新事件
        # self.title_update()

    def add_unit_title(self, news_dict, news_title_dict):
        """
        事件表示，提取事件单元的标题，
        :param self:
        :param news_dict:
        :param news_title_dict:
        :return:
        """
        node_list = self.node_list
        distance_list = []
        # print 'first node: %s' % node_list[0]
        # 事件单元中第一节点的td-idf
        node0_tf_idf = tfidf.load_tfidf_vectorizer([news_dict[node_list[0]]]).toarray().reshape(-1)
        max_dist = singlePassCluster.cosine_distance(self.centroid, node0_tf_idf)
        distance_list.append(max_dist)
        topic_node = node_list[0]
        for node_index, node in enumerate(node_list[1:]):
            # print 'event node: %s' % node
            # 计算每个节点的空间向量
            node_tf_idf = tfidf.load_tfidf_vectorizer([news_dict[node]]).toarray().reshape(-1)
            # 计算每个节点到簇心的欧式距离
            temp_dist = singlePassCluster.cosine_distance(self.centroid, node_tf_idf)
            distance_list.append(temp_dist)
            # 读取相似度最大的节点
            if temp_dist >= max_dist:
                max_dist = temp_dist
                topic_node = node
        # print "distance_list: %s" % distance_list
        # print "max_distance: %s" % max_dist
        # print "topic_node: %s" % topic_node
        # 返回相似度最大的节点对应的新闻标题
        self.topic_title = news_title_dict[topic_node]
        print "[事件标题]: \n%s" % self.topic_title

    def event_expression(self, news_title_list, news_list):
        """
        事件表示，提取事件单元中涉及的股票，提取事件单元中新闻的关键词（所有新闻一起提取）
        :return:
        """
        # 根据事件类簇中的新闻id，从原始
        stock_lists = []
        news_lists = []
        for news in news_list:
            # print news
            # 提取正文中提及到的股票代码
            content_list = news.split(" ")
            stock_list = data_process.find_stocks(content_list=content_list, stock_dicts=dicts.stock_dict)
            stock_lists.extend(stock_list)
            news_lists.extend(content_list)
        # 事件中涉及的股票
        stocks = ",".join(item for item in set(stock_lists))
        print "[事件中包含的股票]: %s " % stocks

        # 事件簇关健词提取
        event_new_string = ' '.join(item for item in news_lists)
        # print "事件类簇 %s" % event_new_string
        event_keywords_list = keywords_extractor.parallel_test(news_lists)
        event_keywords = ','.join(item for item in event_keywords_list)
        print "[事件关键词]:\n %s " % event_keywords

        # 事件表示,事件要素抽取
        # 事件包含的新闻正文
        print '[事件包含的新闻正文]:'
        for news in news_list:
            print news

        # 事件包含的新闻标题
        print '[事件包含的新闻标题]:'
        for news_title in news_title_list:
            print news_title
        self.stocks = stock_lists
        self.keywords = event_keywords

    def title_update(self, node_news_dict):
        """
        对每天更新后的事件单元做title更新
        :return:
        """
        # 事件标题更新
        print "事件标题更新"
        node_list = self.node_list
        distance_list = []
        # print 'first node: %s' % node_list[0]
        # 事件单元中第一节点的td-idf
        first_node = node_news_dict[node_list[0]]
        node0_tf_idf = first_node[1]
        # node0_tf_idf = tfidf.load_tfidf_vectorizer([first_node[1]]).toarray().reshape(-1)
        max_dist = singlePassCluster.cosine_distance(self.centroid, node0_tf_idf)
        distance_list.append(max_dist)
        topic_node = node_list[0]
        for node_index, node in enumerate(node_list[1:]):
            # print 'event node: %s' % node
            # 计算每个节点的空间向量
            node_tf_idf = node_news_dict[node][1]
            # node_tf_idf = tfidf.load_tfidf_vectorizer([node_news_dict[node]]).toarray().reshape(-1)
            # 计算每个节点到簇心的欧式距离
            temp_dist = singlePassCluster.cosine_distance(self.centroid, node_tf_idf)
            distance_list.append(temp_dist)
            # 读取相似度最大的节点
            if temp_dist >= max_dist:
                max_dist = temp_dist
                topic_node = node
        # 返回相似度最大的节点对应的新闻标题
        self.topic_title = node_news_dict[topic_node][3]
        print "更新后的事件标题： %s" % self.topic_title

    def keywords_update(self):
        # 关键词更新
        pass

    def remove_node(self, node):
        ClusterUnit.remove_node(self, node)
        # self.title_update()


class EventLib():
    def __init__(self):
        self.event_unit_list = []
