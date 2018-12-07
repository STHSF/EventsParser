#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: cluster.py
@time: 2018/11/6 1:35 PM
聚类模块
"""
from sklearn.cluster import KMeans


def cluster(x_train):
    infered_vectors_list = []
    print "load doc2vec model..."
    model_dm = Doc2Vec.load("model/model_dm")
    print "load train vectors..."
    i = 0
    for text, label in x_train:
        vector = model_dm.infer_vector(text)
        infered_vectors_list.append(vector)
        i += 1

    print "train kmean model..."
    kmean_model = KMeans(n_clusters=15)
    kmean_model.fit(infered_vectors_list)
    labels = kmean_model.predict(infered_vectors_list[0:100])
    cluster_centers = kmean_model.cluster_centers_

    with open("out/own_claasify.txt", 'w') as wf:
        for i in range(100):
            string = ""
            text = x_train[i][0]
            for word in text:
                string = string + word
            string = string + '\t'
            string = string + str(labels[i])
            string = string + '\n'
            wf.write(string)

    return cluster_centers