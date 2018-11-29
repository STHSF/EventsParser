#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: mainProcess.py
@time: 2018/11/14 3:33 PM
"""
import os
import pickle
import dataReader
import pandas as pd
import numpy as np
from gensim.models.word2vec import Word2Vec
from utills.Tokenization import load_stop_words
from utills.DataProcess import DataPressing
from utills import Tokenization, dicts, Vector
from utills import keywordsExtractor
from utills import news
from multiprocessing import Pool
from src.cluster.singlePass.singlePassCluster import *
from utills import tfidf


def import_title(corpus_path):
    text_dict = {}
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 3:
            category = line[0]
            words = line[2]
            text_dict[category] = words
    return text_dict


def get_news(text_dict, node_list):
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

# # 读取原文本
corpus_train = "/Users/li/PycharmProjects/event_parser/src/text_title.txt"
corpus_dict = import_title(corpus_train)
for cluster_index, cluster in enumerate(clustering.cluster_list):
    print "cluster: %s" % cluster_index  # 簇的序号
    print cluster.node_list  # 该簇的节点列表

    txt_lists = get_news(corpus_dict, cluster.node_list)
    for tmp in txt_lists:
        print tmp

