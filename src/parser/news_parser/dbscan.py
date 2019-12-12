#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: dbscan.py
@time: 2018/10/31 10:51 AM
"""

from sklearn import cluster
from sklearn.metrics import adjusted_rand_score
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn import mixture
from sklearn.svm.libsvm import predict


def create_data(centers, num=100, std=0.7):
    # 产生数据
    X, labels_true = make_blobs(n_samples=num, centers=centers, cluster_std=std)
    return X, labels_true


def plot_data(*data):
    """
        数据作图
    """
    X,labels_true = data
    labels=np.unique(labels_true)
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    colors='rgbycm'
    for i,label in enumerate(labels):
        position=labels_true==label
        ax.scatter(X[position,0],X[position,1],label="cluster %d"%label),
        color=colors[i%len(colors)]

    ax.legend(loc="best",framealpha=0.5)
    ax.set_xlabel("X[0]")
    ax.set_ylabel("Y[1]")
    ax.set_title("data")
    plt.show()


# 测试函数
def test_DBSCAN(*data):
    X,labels_true = data
    clst = cluster.DBSCAN()
    predict_labels = clst.fit_predict(X)
    print("ARI:%s"%adjusted_rand_score(labels_true, predict_labels))
    print("Core sample num:%d"%len(clst.core_sample_indices_))


def test_DBSCAN_epsilon(*data):
    X,labels_true = data
    epsilons = np.logspace(-1,1.5)
    ARIs=[]
    Core_nums = []
    for epsilon in epsilons:
        clst = cluster.DBSCAN(eps=epsilon)
        predicted_labels = clst.fit_predict(X)
        ARIs.append(adjusted_rand_score(labels_true,predicted_labels))
        Core_nums.append(len(clst.core_sample_indices_))

    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(1,2,1)
    ax.plot(epsilons,ARIs,marker = '+')
    ax.set_xscale('log')
    ax.set_xlabel(r"$\epsilon$")
    ax.set_ylim(0,1)
    ax.set_ylabel('ARI')

    ax = fig.add_subplot(1,2,2)
    ax.plot(epsilons,Core_nums,marker='o')
    ax.set_xscale('log')
    ax.set_xlabel(r"$\epsilon$")
    ax.set_ylabel('Core_num')

    fig.suptitle("DBSCAN")
    plt.show()


def test_DBSCAN_min_samples(*data):
    X,labels_true=data
    min_samples = range(1,100)
    ARIs = []
    Core_nums = []
    for num in min_samples:
        clst = cluster.DBSCAN(min_samples=num)
        predicted_labels = clst.fit_predict(X)
        ARIs.append(adjusted_rand_score(labels_true, predicted_labels))
        Core_nums.append(len(clst.core_sample_indices_))

    fig=plt.figure(figsize=(10,5))
    ax=fig.add_subplot(1,2,1)
    ax.plot(min_samples,ARIs,marker='+')
    ax.set_xlabel("min_samples")
    ax.set_ylim(0,1)
    ax.set_ylabel('ARI')

    ax=fig.add_subplot(1,2,2)
    ax.plot(min_samples,Core_nums,marker='o')
    ax.set_xlabel("min_samples")
    ax.set_ylabel('Core_nums')

    fig.suptitle("DBSCAN")
    plt.show()


if __name__ == '__main__':
    X, labels_true = create_data(4)
    # plot_data(data)
    test_DBSCAN(X,labels_true)

    centers = [[1,1],[1,2],[2,2],[10,20]]
    X,labels_true = create_data(centers,1000,0.5)
    test_DBSCAN_epsilon(X, labels_true)

    centers = [[1,1],[1,2],[2,2],[10,20]]
    X,labels_true = create_data(centers,1000,0.5)
    test_DBSCAN_min_samples(X,labels_true)