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
from utills.Tokenization import load_stop_words
from utills.DataProcess import DataPressing
from utills import keywordsExtractor

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
    sql = "SELECT distinct content, title, unix_time FROM xavier_db.%s  ORDER BY unix_time" % sheet_name
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


def data_save():
    """
    读取数据库中的内容，文本预处理之后，保存成本地，用于词向量训练，关键词提取等操作
    :return:
    """
    data_process, dict_init, stop_words = DataPressing(), dicts.init(), load_stop_words()
    tk = Tokenization.Tokenizer(data_process, dict_init, stop_words)  # 分词

    sql_list = ["ths_news", "ycj_news", "xueqiu_news"]
    df_set = []
    # 将所有新闻以dataframe的格式合并
    for index in sql_list:
        df = get_full_data(index)
        df_set.append(df)
    df_result = pd.concat(df_set, join="inner")
    # df_result.ix[:, ["content"]].apply(tk.token)
    # 提取dataframe中的title和content的内容，然后分别进行预处理，

    # 方式一、标题和正文保存为同一个新闻，且新闻标题和正文同时存在
    res_lists = []
    for i in range(len(df_result)):
        title = df_result.iloc[i]['title']
        content = df_result.iloc[i]['content']
        unix_time = df_result.iloc[i]['unix_time']
        if content and title:
            string = title.strip()
            # string = title.strip() + content.strip()
            string_list = tk.token(string)
            if not data_process.useless_filter(string_list, dicts.stock_dict):
                keyword_list = keywordsExtractor.paralize_test(string_list)
                res_lists.append((string, keyword_list, unix_time))  # 将正文

    file_out = open("text_title_cut.txt", "w")
    for index, content in enumerate(res_lists):
        item = ",".join(item for item in content[1])
        # file_out.write(str(index) + "\t" + str(content[2]) + "\t" + content[0].encode("utf8") + "\n")
        file_out.write(str(index) + "\t" + str(content[2]) + "\t" + item.encode("utf8") + "\n")
    file_out.close()

    # # # 方式二、标题和正文保存为同一个新闻
    # res_lists = []
    # for i in range(len(df_result)):
    #     title = df_result.iloc[i]['title']
    #     if title is None:
    #         title = ''
    #     content = df_result.iloc[i]['content']
    #     if content is None:
    #         content = ''
    #     string = title.strip() + content.strip()
    #     if not data_process.useless_filter(string, dicts.stock_dict):
    #         string_list = tk.token(string)
    #         keyword_list = keywordsExtractor.paralize_test(string_list)
    #         res_lists.append(keyword_list)
    #
    # file_out = open("text.txt", "w")
    # for index, content in enumerate(res_lists):
    #     item = ",".join(item for item in content)
    #     file_out.write(str(index) + "\t" + item.encode("utf8") + "\n")
    # file_out.close()

    # 方式三、标题和正文分开保存
    # for index, row in df_result.iterrows():
    #     title, content = row["title"], row["content"]
    #     if title is not None and title:
    #         title = data_process.no_remove(title)
    #         if not data_process.useless_filter(title, dicts.stock_dict):
    #             title_list = tk.token(title)
    #             res_lists.append(title_list)
    #
    #     if content is not None and content:
    #         content = data_process.no_remove(content)
    #         if not data_process.useless_filter(content, dicts.stock_dict):
    #             content_list = tk.token(content)
    #             res_lists.append(content_list)
    #
    # file_out = open("text.txt", "w")
    # for index, content in enumerate(res_lists):
    #     item = ",".join(item for item in content)
    #     file_out.write(str(index) + "\t" + item.encode("utf8") + "\n")
    # file_out.close()


if __name__ == '__main__':
    # load_data_test()
    data_save()
