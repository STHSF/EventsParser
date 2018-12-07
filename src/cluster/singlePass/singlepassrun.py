#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: singlepassrun.py
@time: 2018/11/29 8:04 PM
"""

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from src.cluster.singlePass.singlePassCluster import *
from src.utills import tfidf
import pickle

corpus_train = "/Users/li/PycharmProjects/event_parser/src/data/text_full_full.txt"
# tfidf_train, word_dict = tfidf_vector(corpus_train)
tfidf_train, word_dict = tfidf.tfidf_vector(corpus_train)
# print np.shape(tfidf_train.toarray())
# print tfidf_train.toarray()[1]

clustering = OnePassCluster(vector_list=tfidf_train.toarray(), threshold=10)
clustering.print_result()

# 将聚好的类簇保存下来，为后面的事件表示和有效事件判断使用。
path = "/Users/li/PycharmProjects/event_parser/src/"
clustering_path = path + 'model/clustering.pkl'
with open(clustering_path, 'wb') as fw:
    pickle.dump(clustering, fw)

# for cluster_index, cluster in enumerate(cluster_list):
#     print "cluster:%s" % cluster_index  # 簇的序号
#     print cluster.node_list  # 该簇的节点列表