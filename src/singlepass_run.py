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
import numpy as np
from configure import conf
from utils import tfidf, log
from cluster.singlePass import singlePassCluster

logging = log.Logger('singlepass_run')
# corpus_train_path = "/Users/li/PycharmProjects/event_parser/src/data/text_full_index.txt"
corpus_train_path = conf.corpus_train_path
# tfidf_train, word_dict = tfidf_vector(corpus_train)
# tfidf_train, word_dict = tfidf.tfidf_vector(corpus_train)
corpus_train_dict = tfidf.load_data(corpus_train_path)

# load tf-idf VSM
tfidf_feature_path = conf.tfidf_feature_path
tfidf_transformer_path = conf.tfidftransformer_path

try:
    tfidf_feature = tfidf.load_tfidf_feature(tfidf_feature_path)
    tfidf_transformer = tfidf.load_tfidf_transformer(tfidf_transformer_path)
    logging.logger.info("TF-IDF model load sucess")
except:
    logging.logger.info("TF-IDF model load failed, please check path %s,%s" % (tfidf_feature_path,
                                                                               tfidf_transformer_path))
    sys.exit()

tfidf_train_tuple = tfidf.load_batch_tfidf_vector(corpus_train_dict, tfidf_feature, tfidf_transformer)

# tfidf_train_tuple = []
# for item in corpus_train_dict.items():
#     catagory, corpus = item[1], item[0]
#     tfidf_train_tuple.append((catagory, tfidf.load_tfidf_vectorizer([corpus], tfidf_feature, tfidf_transformer)))

# tfidf_train_dict, tfidf_train_tuple2, word_dict = tfidf.tfidf_vectorizer(corpus_train_path)
logging.logger.info('tfidf load success')
# print np.shape(tfidf_train.toarray())
# print tfidf_train.toarray()[1]

# clustering = OnePassCluster(vector_tuple=tfidf_train.toarray(), threshold=10)
# clustering = singlePassCluster.OnePassCluster(vector_tuple=tfidf_train_tuple, threshold=10)
clustering = singlePassCluster.OnePassCluster(vector_tuple=tfidf_train_tuple, threshold=20)
clustering.print_result()

# 将聚好的类簇保存下来，为后面的事件表示和有效事件判断使用。
# clustering_path = '/Users/li/PycharmProjects/event_parser/src/model/clustering_new.pkl'
clustering_path = conf.clustering_save_path
with open(clustering_path, 'wb') as fw:
    pickle.dump(clustering, fw)
logging.logger.info("cluster units save success in path{}".format(clustering_path))
# for cluster_index, cluster in enumerate(cluster_list):
#     print "cluster:%s" % cluster_index  # 簇的序号
#     print cluster.node_list  # 该簇的节点列表
