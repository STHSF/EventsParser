#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: singlepass_test.py
@time: 2018-12-27 20:38
"""


import sys
import numpy as np
sys.path.append('..')
sys.path.append('../')
sys.path.append('../../')
from src.configure import conf
from src.utils import tfidf, log_util

logging = log_util.Logger('singlepass_test')
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
# 计算历史新闻文本的TF-IDF，并与news_id组成tuple
tfidf_train_tuple = tfidf.load_batch_tfidf_vector(corpus_train_dict, tfidf_feature, tfidf_transformer)
logging.logger.info('TF-IDF of news calculate success')

# tfidf_train_tuple = []
# for item in corpus_train_dict.items():
#     catagory, corpus = item[1], item[0]
#     tfidf_train_tuple.append((catagory, tfidf.load_tfidf_vectorizer([corpus], tfidf_feature, tfidf_transformer)))

tfidf_train_dict, tfidf_train_tuple2, word_dict = tfidf.tfidf_vectorizer(corpus_train_path)

# for i in tfidf_train_tuple[0][1]:
#     print i
print(np.nonzero(tfidf_train_tuple[0][1]))
print(np.nonzero(tfidf_train_tuple2[0][1]))

print(tfidf_train_tuple[0][1] == np.nonzero(tfidf_train_tuple2[0][1]))

# for i in dict(tfidf_train_tuple).items():
#     print i[0]