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
    # 遍历文件夹下的所有文件，包含子目录里面的文件
    pass


def get_news_data():
    data_path = '/Users/li/PycharmProjects/event_parser/src/text.txt'
    with open(data_path, 'r') as news:
        data = news.readlines()
    train_data = []
    for i, text in enumerate(data):
        text_list = text.decode("utf8").split(",")
        train_data.append(text_list)
    return train_data


def get_datasest():
    with open("/Users/li/PycharmProjects/event_parser/src/corpus/体育", 'r') as cf:
        docs = cf.readlines()
    x_train = []
    # y = np.concatenate(np.ones(len(docs)))
    for i, text in enumerate(docs):
        word_list = text.decode("utf8").split(' ')
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


def load_data_test():
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
    file_out = open("text.txt", "w")
    for index in res_lists:
        item = ",".join(item for item in index)
        file_out.write(item.encode("utf8") + "\n")
    file_out.close()


if __name__ == '__main__':
    # load_data_test()
    a1 = get_news_data()
    a2 = get_datasest()

    print np.shape(a1[0])
    print np.shape(a2[0])

    print a1[0]
    print a2[0]
