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


def tfidf_vector(corpus_path):
    """vectorize the input documents"""
    corpus_train = []
    # 利用train-corpus提取特征
    target_train = []
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 2:
            words = line[1]
            category = line[0]
            target_train.append(category)
            corpus_train.append(words)
    print "build train-corpus done!!"
    count_v1 = CountVectorizer(max_df=0.4, min_df=0.01)
    # count_v1 = CountVectorizer()
    counts_train = count_v1.fit_transform(corpus_train)

    word_dict = {}
    for index, word in enumerate(count_v1.get_feature_names()):
        word_dict[index] = word

    print "the shape of train is " + repr(counts_train.shape)
    tfidftransformer = TfidfTransformer()
    tfidf_train = tfidftransformer.fit(counts_train).transform(counts_train)
    return tfidf_train, word_dict


if __name__=='__main__':
    corpus_train = "/Users/li/PycharmProjects/event_parser/src/text.txt"
    # tfidf_train, word_dict = tfidf_vector(corpus_train)
    tfidf_train, word_dict = tfidf.tfidf_vector(corpus_train)
    # print np.shape(tfidf_train.toarray())
    # print tfidf_train.toarray()[1]

    clustering = OnePassCluster(vector_list=tfidf_train.toarray(), threshold=14)
    cluster_list = clustering.print_result()
    for cluster_index, cluster in enumerate(cluster_list):
        print "cluster:%s" % cluster_index  # 簇的序号
        print cluster.node_list  # 该簇的节点列表

