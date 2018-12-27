#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: tfidf.py
@time: 2018/11/28 4:03 PM
"""
import sys

sys.path.append('..')
sys.path.append('../')
sys.path.append('../../')
import pickle
import numpy as np
from configure import conf
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def load_data(corpus_path):
    corpus_train_dic = {}
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 3:
            category = line[0]
            words = line[2]
            corpus_train_dic[category] = words
    return corpus_train_dic


def tfidf_vectorizer(corpus_path):
    """vectorize the training documents"""
    corpus_train = []
    category_train = []
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 3:
            category = line[0]
            words = line[2]
            category_train.append(category)
            corpus_train.append(words)
    print "build train-corpus done!!"
    print "corpus_train.shape %s" % np.shape(corpus_train)
    # replace 必须加，保存训练集的特征
    count_vectorizer = CountVectorizer(decode_error="replace")
    # count_vectorizer = CountVectorizer(max_df=0.4, min_df=0.01, decode_error="replace")
    counts_train = count_vectorizer.fit_transform(corpus_train)

    word_dict = {}
    for index, word in enumerate(count_vectorizer.get_feature_names()):
        word_dict[index] = word
    print "The VSM shape of train is" + repr(counts_train.shape)

    tfidftransformer = TfidfTransformer()
    # 注意在训练的时候必须用vectorizer.fit_transform、tfidftransformer.fit_transform
    # 在预测的时候必须用vectorizer.transform、tfidftransformer.transform
    tfidf_train = tfidftransformer.fit_transform(counts_train)
    # tfidf_train = tfidftransformer.fit(counts_train).transform(counts_train)

    tfidf_train_array = tfidf_train.toarray()
    tfidf_train_dict = {}
    for item in range(len(tfidf_train_array)):
        tfidf_train_dict[category_train[item]] = tfidf_train_array[item]

    tfidf_train_tuple = []
    for item in range(len(tfidf_train_array)):
        tfidf_train_tuple.append((category_train[item], tfidf_train_array[item]))

    # 保存经过fit的vectorizer 与 经过fit的tfidftransformer,预测时使用
    # tfidf_feature_path = '/Users/li/PycharmProjects/event_parser/src/model/tfidf_model/feature_1.pkl'
    tfidf_feature_path = conf.tfidf_feature_path
    with open(tfidf_feature_path, 'wb') as fw:
        pickle.dump(count_vectorizer.vocabulary_, fw)

    # tfidftransformer_path = '/Users/li/PycharmProjects/event_parser/src/model/tfidf_model/tfidftransformer_1.pkl'
    tfidftransformer_path = conf.tfidftransformer_path
    with open(tfidftransformer_path, 'wb') as fw:
        pickle.dump(tfidftransformer, fw)

    # word_dict_path = '/Users/li/PycharmProjects/event_parser/src/model/tfidf_model/word_dict_1.pkl'
    word_dict_path = conf.word_dict_path
    with open(word_dict_path, 'wb') as fw:
        pickle.dump(word_dict, fw)

    return tfidf_train_dict, tfidf_train_tuple, word_dict


def load_batch_tfidf_vector(corpus_train_dict, tfidf_feature, tfidf_transformer):
    """
    将语料库中的数据转换成数据
    :param corpus_train_dict:
    :param tfidf_feature:
    :param tfidf_transformer:
    :return:
    """
    tfidf_train_tuple = []
    for item in corpus_train_dict.items():
        catagory, corpus = item[1], item[0]
        tfidf_train_tuple.append((catagory, load_tfidf_vectorizer([corpus], tfidf_feature, tfidf_transformer)))

    return tfidf_train_tuple


def load_tfidf_feature(tfidf_feature_path):
    """
    load tf-idf VSM
    :param tfidf_feature_path:
    :return:
    """
    return pickle.load(open(tfidf_feature_path, "rb"))


def load_tfidf_transformer(tfidf_transformer_path):
    """
    load tf-idf transformer
    :param tfidf_transformer_path:
    :return:
    """
    tfidf_transformer = pickle.load(open(tfidf_transformer_path, "rb"))
    return tfidf_transformer


def load_tfidf_vectorizer(corpus_path, vocab, tfidf_transformer):
    """
    :param tfidf_transformer:
    :param vocab: tf-idf feature
    :param corpus_path:
    :return:
    """
    # if type(corpus_path) is not list:
    #     corpus_test = []
    #     target_test = []
    #     for line in open(corpus_path):
    #         line = line.strip().split('\t')
    #         if len(line) == 3:
    #             category = line[0]
    #             words = line[2]
    #             target_test.append(category)
    #             corpus_test.append(words)
    # else:
    #     corpus_test = corpus_path
    corpus_test = corpus_path
    # 加载特征
    loaded_vec = CountVectorizer(decode_error="replace", vocabulary=vocab)
    # 加载TfidfTransformer
    # 测试用transform，表示测试数据，为list
    test_tfidf = tfidf_transformer.transform(loaded_vec.transform(corpus_test))
    return test_tfidf.toarray().reshape(-1)


def tfidf_vector_test(corpus_path):
    """vectorize the input documents"""
    corpus_train = []
    # 利用train-corpus提取特征
    target_train = []
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 3:
            words = line[2]
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


if __name__ == '__main__':
    # corpus_train = "/Users/li/PycharmProjects/event_parser/src/text_full_full.txt"
    corpus_train = conf.corpus_train_path
    tfidf_train_dic, tfidf_train_tuple, word_dict = tfidf_vectorizer(corpus_train)
    print np.nonzero(tfidf_train_dic["111755669"])
    print np.shape(tfidf_train_dic['111755669'])
    print type(tfidf_train_dic['111755669'])
    # print np.shape(tfidf_train.toarray()[0])
    # print np.nonzero(tfidf_train.toarray()[0])
    # for i in tfidf_train.toarray()[0]:
    #     print i

    # corpus_data_dic = load_data(corpus_train)
    # print type(corpus_data_dic['111755669'])
    # tfidf_test = load_tfidf_vectorizer([corpus_data_dic['111755669']]).toarray().reshape(-1)
    # print np.nonzero(tfidf_test)
