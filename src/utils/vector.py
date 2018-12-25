#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: vector.py
@time: 2018/11/5 2:31 PM
词向量，文本向量训练模块
训练用的编码格式要与使用model时的编码格式一致。
"""

import sys
import os
sys.path.append("..")
sys.path.append("../")
sys.path.append("../../")
import logging.handlers
import my_util
import numpy as np
import multiprocessing
from gensim.models.word2vec import Word2Vec
from gensim.models.doc2vec import Doc2Vec, LabeledSentence
import dataReader

LOG_FILE = '../log/vectors.log'
my_util.check_path(LOG_FILE)
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=1)  # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
# logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(level=logging.INFO)
# logger.setLevel(level=logging.DEBUG)
logger.info("running %s" % ' '.join(sys.argv))


class word2vecs(object):
    def __init__(self, wd_configure):
        """
        参数初始化
        :param wd_configure: 模型的参数
        """

        if "size" in wd_configure.keys():
            # 训练时词向量维度，默认为100
            self.size = wd_configure["size"]
        else:
            self.size = 300

        if "min_count" in wd_configure.keys():
            # min_count 不能设置过大，不然词汇表中会没有词汇
            # 需要训练词语的最小出现次数，默认为5
            self.min_count = wd_configure["min_count"]
        else:
            self.min_count = 1

        if "window" in wd_configure.keys():
            self.window = wd_configure["window"]
        else:
            self.window = 5

        if "worker" in wd_configure.keys():
            # 完成训练过程的线程数，默认为1不使用多线程， 只有注意安装Cython的前提下该参数设置才有意义
            self.worker = wd_configure["worker"]
        else:
            self.worker = multiprocessing.cpu_count()

    def train(self, sentences):
        """
        模型训练
        :param sentences:每行为一个list 如sentences = [['A1', 'A2'], ['A1', 'A2'], ['A1', 'A2', 'A1', 'A2']]
        :return: word2vec 模型
        # """
        model_w2d = Word2Vec(size=self.size, window=self.window, min_count=self.min_count, workers=self.worker)
        model_w2d.build_vocab(sentences)
        model_w2d.train(sentences, total_examples=model_w2d.corpus_count, epochs=model_w2d.iter)
        return model_w2d

    def save(self, model, model_path):
        model.save(model_path)

    def load_model(self, model_path):
        return Word2Vec.load(model_path)


class doc2vec(object):
    def __init__(self, dm_configure):
        if dm_configure.min_count:
            self.min_count = dm_configure.min_count
        else:
            self.min_count = 1

        if dm_configure.window:
            self.window = dm_configure.window
        else:
            self.window = 3

        if dm_configure.size:
            self.size = dm_configure.size
        else:
            self.size = 200

        if dm_configure.sample:
            self.sample = dm_configure.sample
        else:
            self.sample = 1e-3

        if dm_configure.negative:
            self.negative = dm_configure.negative
        else:
            self.negative = 5

        if dm_configure.workers:
            self.workers = dm_configure.workers
        else:
            self.workers = multiprocessing.cpu_count()

    def train(self, x_train):
        model_dm = Doc2Vec(x_train, min_count=self.min_count, window=self.window, size=self.size,
                           sample=self.sample, negative=self.negative, workers=self.workers)
        model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=100)

        return model_dm

    def save(self, model_dm, model_path):
        # model_dm.save('../model/model_dm')
        model_dm.save(model_path)  # model_dm.load(model_path)
        # model_dm.save_word2vec_format(model_path)  # model_dm.load_word2vec_format(model_path,encoding='utf-8')

    # def train(x_train, size=200, epoch_num=1):
    #     model_dm = Doc2Vec(x_train, min_count=1, window=3, size=size, sample=1e-3, negative=5, workers=4)
    #     model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=100)
    #     model_dm.save('../model/model_dm')
    #
    #     return model_dm


def word2vec_train(self):
    # load training data
    x_train = dataReader.get_news_data()
    # word2vec 训练测试
    wd_configure = {"size": 300,
                    "window": 2,
                    "min_count": 1}
    wd = word2vecs(wd_configure)
    model_wd = wd.train(x_train)
    print("[Info] word2vec模型训练结束")
    logger.info("[Info] word2vec模型训练结束")
    print model_wd.wv[u'食品饮料']
    # print model_wd.most_similar['食品饮料']

    # 模型保存
    model_path = "/Users/li/PycharmProjects/event_parser/src/model/model_300_2_1"
    if not os.path.exists(model_path):
        wd.save(model_wd, model_path)
    else:
        print("[Exception] word2vec的保存路径已经存在。")


def word2vec_load(model_path=None):
    """
    load word2vec model
    :return:
    """
    if model_path:
        model_path = model_path
    else:
        model_path = "/Users/li/PycharmProjects/event_parser/src/model/model_300_2_1"

    wd_conf = {"size": 300,
                "window": 5,
                "min_count": 1}
    model_wd = word2vecs(wd_conf)
    model_wd = model_wd.load_model(model_path)
    # print model_wd.wv[u'食饮料']
    return model_wd


def word_vector(word, w2v_model):
    """
    查找某个词的词向量
    :param word: 需要查找的词
    :param w2v_model: 词向量 shape = (vector_size, )
    :return:
    """
    try:
        vector = w2v_model.wv[word]
        return vector
    except KeyError:
        return np.zeros(w2v_model.vector_size)


if __name__ == '__main__':
    model_path = "/Users/li/PycharmProjects/event_parser/src/model/model_300_2_1"

    # word2vec 训练测试
    wd_conf = {"size": 300,
               "window": 5,
               "min_count": 1}
    x_train = dataReader.get_datasest()
    wd = word2vecs(wd_conf)
    model_wd = wd.train(x_train)
    print model_wd.wv[u'球员']

    # doc2vec 训练测试
    # cluster_centers = cluster(x_train)
