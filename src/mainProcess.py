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
from utills import Tokenization, DataProcess, dicts, Vector


class mainProcess(object):

    def data_save(self):
        tk = Tokenization.Tokenizer()
        dp = DataProcess.DataPressing()

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
                title = dp.no_remove(title)
                if not dp.useless_filter(title, dicts.stock_dict):
                    title_list = tk.token(title)
                    res_lists.append(title_list)

            if content is not None and content:
                content = dp.no_remove(content)
                if not dp.useless_filter(content, dicts.stock_dict):
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
        wd = Vector.word2vec(wd_configure)
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


if __name__ == '__main__':
    mp = mainProcess()
    mp.data_save()
    mp.word2vec_train()