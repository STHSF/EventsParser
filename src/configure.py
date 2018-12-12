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

    path = "/Users/li/PycharmProjects/event_parser/src/"

    # 停用词目录
    stop_words_path = '/Users/li/PycharmProjects/event_parser/src/corpus/stop_words_CN'

    # tf-idf 训练语料文件位置
    corpus_train_path = "/Users/li/PycharmProjects/event_parser/src/data/text_full_index.txt"


    #
    clustering_save_path = path + 'model/clustering_new.pkl'

    #
    event_save_path = ''


