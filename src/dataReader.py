#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: dataReader.py
@time: 2018/10/30 7:05 PM
"""
import sys
sys.path.append('..')
import gensim
import numpy as np
import pandas as pd
from utills.DataSource import GetDataEngine
from utills import Tokenization, DataProcess, dicts

TaggededDocument = gensim.models.doc2vec.TaggedDocument

engine_mysql = GetDataEngine("XAVIER")
global _stopwords


def list_all_flies(root_path):
    pass


def get_news_data():
    data_path = ''
    with open(data_path, 'r') as news:
        pass


def get_datasest():
    with open("/Users/li/PycharmProjects/huihongcaihui/src/corpus/体育", 'r') as cf:
        docs = cf.readlines()
    x_train = []
    # y = np.concatenate(np.ones(len(docs)))
    for i, text in enumerate(docs):
        word_list = text.split(' ')
        # l = len(word_list)
        # word_list[l - 1] = word_list[l - 1].strip()
        # document = TaggededDocument(word_list, tags=[i])
        x_train.append(word_list)
    return x_train


def get_full_data(sheet_name):
    """
    :return:
    """
    # sql = "SELECT title, content FROM xavier_db.%s LIMIT 10" % sheet_name
    sql = "SELECT title, content FROM xavier_db.%s" % sheet_name
    df_result = pd.read_sql(sql, engine_mysql)
    return df_result


'''
df = pd.read_csv('体育.csv')
sentences = df['doc']
line_sent = []
for s in sentences:
    line_sent.append(s.split())  #句子组成list
'''


if __name__ == '__main__':
    tk = Tokenization.Tokenizer()
    dp = DataProcess.DataPressing()

    sql_list = ["ths_news", "ycj_news", "xueqiu_news"]
    df_set = []
    # 将所有新闻合并
    for index in sql_list:
        df = get_full_data(index)
        df_set.append(df)
    df_result = pd.concat(df_set, join="inner")
    # df_result.ix[:, ["content"]].apply(tk.token)

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
    file = open("text.txt", "w")

    for index in res_lists:
        file.write(str(index) + "\n")

        # str = ""
        # for item in index:
        #     str += item + "\n"
        # str
    file.close()
    # print np.shape(res_lists[0])
    # for i in res_lists[0]:
    #     print i