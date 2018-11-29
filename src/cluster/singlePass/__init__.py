#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: __init__.py.py
@time: 2018/11/28 3:49 PM
"""
import sys
sys.path.append("../../")

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from src.cluster.singlePass.singlePassCluster import *
from utills import tfidf


corpus_train = "/Users/li/PycharmProjects/event_parser/src/text.txt"
# tfidf_train, word_dict = tfidf_vector(corpus_train)
tfidf_train, word_dict = tfidf.tfidf_vector(corpus_train)
# print np.shape(tfidf_train.toarray())
# print tfidf_train.toarray()[1]

clustering = OnePassCluster(vector_list=tfidf_train.toarray(), threshold=15)
clustering.print_result()

# for cluster_index, cluster in enumerate(cluster_list):
#     print "cluster:%s" % cluster_index  # 簇的序号
#     print cluster.node_list  # 该簇的节点列表

