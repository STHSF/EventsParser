#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: singlepass_run.py
@time: 2018/11/29 8:04 PM
新闻聚类
"""
import sys
sys.path.append('..')
sys.path.append('../')
sys.path.append('../../')
import pickle
from configure import conf
from utils import tfidf
from cluster.singlePass import singlePassCluster

# corpus_train_path = "/Users/li/PycharmProjects/event_parser/src/data/text_full_index.txt"
corpus_train_path = conf.corpus_train_path
# tfidf_train, word_dict = tfidf_vector(corpus_train)
# tfidf_train, word_dict = tfidf.tfidf_vector(corpus_train)
tfidf_train_dict, tfidf_train_tuple, word_dict = tfidf.tfidf_vector(corpus_train_path)
# print np.shape(tfidf_train.toarray())
# print tfidf_train.toarray()[1]

# clustering = OnePassCluster(vector_tuple=tfidf_train.toarray(), threshold=10)
# clustering = singlePassCluster.OnePassCluster(vector_tuple=tfidf_train_tuple, threshold=10)
clustering = singlePassCluster.OnePassCluster(vector_tuple=tfidf_train_tuple, threshold=40)
clustering.print_result()

# 将聚好的类簇保存下来，为后面的事件表示和有效事件判断使用。
# clustering_path = '/Users/li/PycharmProjects/event_parser/src/model/clustering_new.pkl'
clustering_path = conf.clustering_save_path
with open(clustering_path, 'wb') as fw:
    pickle.dump(clustering, fw)

# for cluster_index, cluster in enumerate(cluster_list):
#     print "cluster:%s" % cluster_index  # 簇的序号
#     print cluster.node_list  # 该簇的节点列表