#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: tfidf.py
@time: 2018/11/28 4:03 PM

"""

import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


path = "/Users/li/PycharmProjects/event_parser/src/"


def load_data(corpus_path):
    corpus_train_dic = {}
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 3:
            category = line[0]
            words = line[2]
            corpus_train_dic[category] = words
    return corpus_train_dic


def tfidf_vector(corpus_path):
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
    print "the shape of train is" + repr(counts_train.shape)

    tfidftransformer = TfidfTransformer()
    # 注意在训练的时候必须用vectorizer.fit_transform、tfidftransformer.fit_transform
    # 在预测的时候必须用vectorizer.transform、tfidftransformer.transform
    tfidf_train = tfidftransformer.fit_transform(counts_train)
    # tfidf_train = tfidftransformer.fit(counts_train).transform(counts_train)

    tfidf_train_array = tfidf_train.toarray()
    tfidf_train_dict = []
    for item in range(len(tfidf_train_array)):
        tfidf_train_dict.append((category_train[item], tfidf_train_array[item]))

    # 保存经过fit的vectorizer 与 经过fit的tfidftransformer,预测时使用
    feature_path = path + 'model/tfidf_model/feature_1.pkl'
    with open(feature_path, 'wb') as fw:
        pickle.dump(count_vectorizer.vocabulary_, fw)

    tfidftransformer_path = path + 'model/tfidf_model/tfidftransformer_1.pkl'
    with open(tfidftransformer_path, 'wb') as fw:
        pickle.dump(tfidftransformer, fw)

    word_dict_path = path + 'model/tfidf_model/word_dict_1.pkl'
    with open(word_dict_path, 'wb') as fw:
        pickle.dump(word_dict, fw)

    return tfidf_train_dict, word_dict


def load_tfidf_vectorizer(corpus_path):

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
    feature_path = path + 'model/tfidf_model/feature_1.pkl'
    loaded_vec = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open(feature_path, "rb")))
    # 加载TfidfTransformer
    tfidftransformer_path = path + 'model/tfidf_model/tfidftransformer_1.pkl'
    tfidftransformer = pickle.load(open(tfidftransformer_path, "rb"))
    # 测试用transform，表示测试数据，为list
    test_tfidf = tfidftransformer.transform(loaded_vec.transform(corpus_test))

    return test_tfidf


def tfidf_vector_test(corpus_path):
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


if __name__ == '__main__':
    # corpus_train = "/Users/li/PycharmProjects/event_parser/src/text_full_full.txt"
    corpus_train = "/Users/li/PycharmProjects/event_parser/src/text_full_index.txt"
    tfidf_train_dic, word_dict = tfidf_vector(corpus_train)
    print np.nonzero(tfidf_train_dic['111755669'])
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
