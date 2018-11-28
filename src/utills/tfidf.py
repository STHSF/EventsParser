#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: tfidf.py
@time: 2018/11/28 4:03 PM

"""

import pickle
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def tfidf_vector(corpus_path):
    """vectorize the training documents"""
    corpus_train = []
    target_train = []
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 2:
            category = line[1]
            words = line[1]
            target_train.append(category)
            corpus_train.append(words)
    print "build train-corpus done!!"
    # replace 必须加，保存训练集的特征
    count_vectorizer = CountVectorizer(max_df=0.4, min_df=0.01, decode_error="replace")
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

    # 保存经过fit的vectorizer 与 经过fit的tfidftransformer,预测时使用
    feature_path = '../model/tfidf_model/feature.pkl'
    with open(feature_path, 'wb') as fw:
        pickle.dump(count_vectorizer.vocabulary_, fw)

    tfidftransformer_path = '../model/tfidf_model/tfidftransformer.pkl'
    with open(tfidftransformer_path, 'wb') as fw:
        pickle.dump(tfidftransformer, fw)

    word_dict_path = '../model/tfidf_model/word_dict.pkl'
    with open(word_dict_path, 'wb') as fw:
        pickle.dump(word_dict, fw)

    return tfidf_train, word_dict


def load_tfidf_vectorizer(corpus_path):
    corpus_test = []
    target_test = []
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 2:
            category = line[1]
            words = line[1]
            target_test.append(category)
            corpus_test.append(words)

    # 加载特征
    feature_path = '../model/tfidf_model/feature.pkl'
    loaded_vec = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open(feature_path, "rb")))
    # 加载TfidfTransformer
    tfidftransformer_path = '../model/tfidf_model/tfidftransformer.pkl'
    tfidftransformer = pickle.load(open(tfidftransformer_path, "rb"))
    # 测试用transform，表示测试数据，为list
    test_tfidf = tfidftransformer.transform(loaded_vec.transform(corpus_test))

    return test_tfidf


if __name__=='__main__':
    corpus_train = "/Users/li/PycharmProjects/event_parser/src/text.txt"
    tfidf_train, word_dict = tfidf_vector(corpus_train)
    # tfidf_test = load_tfidf_vectorizer(corpus_train)