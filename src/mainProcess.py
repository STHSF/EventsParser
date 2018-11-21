#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: mainProcess.py
@time: 2018/11/14 3:33 PM
"""
import os
import dataReader
import pandas as pd
import numpy as np
from gensim.models.word2vec import Word2Vec
from utills.Tokenization import load_stop_words
from utills.DataProcess import DataPressing
from utills import Tokenization, dicts, Vector


class mainProcess(object):

    def data_save(self):
        """
        读取数据库中的内容，文本预处理之后，保存成本地，用于词向量训练
        :return:
        """
        data_process, dict_init, stop_words = DataPressing(), dicts.init(), load_stop_words()
        tk = Tokenization.Tokenizer(data_process, dict_init, stop_words)  # 分词

        sql_list = ["ths_news", "ycj_news", "xueqiu_news"]
        df_set = []
        # 将所有新闻以dataframe的格式合并
        for index in sql_list:
            df = dataReader.get_full_data(index)
            df_set.append(df)
        df_result = pd.concat(df_set, join="inner")
        # df_result.ix[:, ["content"]].apply(tk.token)
        # 提取dataframe中的title和content的内容，然后分别进行预处理，
        res_lists = []
        for index, row in df_result.iterrows():
            title, content = row["title"], row["content"]
            if title is not None and title:
                title = data_process.no_remove(title)
                if not data_process.useless_filter(title, dicts.stock_dict):
                    title_list = tk.token(title)
                    res_lists.append(title_list)

            if content is not None and content:
                content = data_process.no_remove(content)
                if not data_process.useless_filter(content, dicts.stock_dict):
                    content_list = tk.token(content)
                    res_lists.append(content_list)

        file_out = open("text.txt", "w")
        for index in res_lists:
            item = ",".join(item for item in index)
            file_out.write(item.encode("utf8") + "\n")
        file_out.close()

    def word2vec_train(self):
        # load training data
        x_train = dataReader.get_news_data()
        # word2vec 训练测试
        wd_configure = {"size": 300,
                        "window": 2,
                        "min_count": 1}
        wd = Vector.word2vecs(wd_configure)
        model_wd = wd.train(x_train)
        print("[Info] word2vec模型训练结束")
        print model_wd.wv[u'食品饮料']
        # print model_wd.most_similar['食品饮料']

        # 模型保存
        model_path = "/Users/li/PycharmProjects/event_parser/src/model/model_300_2_1"
        if not os.path.exists(model_path):
            wd.save(model_wd, model_path)
        else:
            print("[Exception] word2vec的保存路径已经存在。")

    def word2vec_load(self, model_path=None):
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
        model_wd = Vector.word2vecs(wd_conf)
        model_wd = model_wd.load_model(model_path)
        # print model_wd.wv[u'食饮料']
        return model_wd

    def word_vector(self, word, w2v_model):
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
    mp = mainProcess()
    # mp.data_save()
    # mp.word2vec_train()
    model_w2v = mp.word2vec_load()
    var = mp.word_vector(u'食品饮料', model_w2v)
    print var
