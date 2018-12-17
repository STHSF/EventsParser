#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: configure.py
@time: 2018/10/31 1:52 PM
配置文件
"""


class Configure(object):
    project_path = "/Users/li/PycharmProjects"

    # 词典目录
    dic_path = project_path + '/event_parser/src/corpus'

    # 停用词目录
    stop_words_path = project_path + '/event_parser/src/corpus/stop_words_CN'

    # tf-idf 训练语料文件位置，标题和正文合并在一起
    corpus_train_path = project_path + "/event_parser/src/data/text_full_index.txt"

    # singlepass聚类结果保存目录文件
    clustering_save_path = project_path + '/event_parser/src/model/clustering_new.pkl'

    corpus_news = corpus_train_path
    # 提取的新闻标题
    corpus_news_title = project_path + "/event_parser/src/data/text_title_index.txt"
    #
    event_unit_path = project_path + '/event_parser/src/model/event_units_new.pkl'
    #
    event_save_path = project_path + '/event_parser/src/model/event_model/'

    # TF-IDF计算相关文件
    tfidf_feature_path = project_path + '/event_parser/src/model/tfidf_model/feature_1.pkl'
    tfidftransformer_path = project_path + '/event_parser/src/model/tfidf_model/tfidftransformer_1.pkl'
    word_dict_path = project_path + '/event_parser/src/model/tfidf_model/word_dict_1.pkl'


conf = Configure()
