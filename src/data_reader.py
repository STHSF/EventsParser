#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: data_reader.py
@time: 2018/10/30 7:05 PM
"""
import time
import gensim
import pandas as pd
from src.configure import conf
from src.utils.data_source import GetDataEngine
from src.utils import tokenization, data_process, dicts
from src.utils.tokenization import load_stop_words
from src.utils import keywords_extractor, time_util, tfidf

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


def get_data_sets():
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


def read_full_data(sheet_name):
    """
    :return:
    """
    # sql = "SELECT title, content FROM xavier_db.%s LIMIT 10" % sheet_name
    sql = "SELECT distinct content, id, title, unix_time FROM xavier_db.%s  ORDER BY unix_time" % sheet_name
    result = pd.read_sql(sql, engine_mysql)
    return result


def read_ordered_data(sheet_name, time_stamp):
    """
    :return:
    """

    timestamp_now = int(time.time())
    # sql = "SELECT title, content FROM xavier_db.%s LIMIT 10" % sheet_name
    sql = "SELECT distinct content, id, title, unix_time FROM xavier_db.%s where unix_time >= %s ORDER BY unix_time" % (sheet_name, time_stamp)

    # sql = "SELECT distinct content, title, unix_time FROM xavier_db.%s where unix_time >= %s AND unix_time <= %s ORDER BY unix_time" % (
    # sheet_name, time_stamp, timestamp_now)
    result = pd.read_sql(sql, engine_mysql)
    return result


'''
df = pd.read_csv('体育.csv')
sentences = df['doc']
line_sent = []
for s in sentences:
    line_sent.append(s.split())  #句子组成list
'''


def get_data():
    """
    获取三张表中的所有新闻
    :return:
    """
    sql_list = ["ths_news", "ycj_news", "xueqiu_news"]
    df_set = []
    # 将所有新闻合并
    for index in sql_list:
        df = read_full_data(index)
        df_set.append(df)
    result = pd.concat(df_set, join="inner")
    # result.ix[:, ["content"]].apply(tk.token)
    return result


def get_ordered_data(timestamp):
    """
    从数据库中搜索指定时间戳
    :return:
    """
    sql_list = ["ths_news", "ycj_news", "xueqiu_news"]
    df_set = []
    # 将所有新闻合并
    for index in sql_list:
        df = read_ordered_data(index, timestamp)
        df_set.append(df)
    result = pd.concat(df_set, join="inner")
    # result.ix[:, ["content"]].apply(tk.token)
    return result


def import_title(corpus_path):
    """
    将新闻的news_id和新闻的标题news_title转换成dict，为后面从类簇中提取节点对应的新闻标题使用
    :param corpus_path: 语料的路径
    :return: dict, {news_id: news_title}
    """
    title_text_dict = {}
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 3:
            category = line[0]
            title = line[2]
            title_text_dict[category] = title
    return title_text_dict


def import_news(corpus_path):
    """
    将新闻的news_id和新闻的正文news转换成dict，为后面从类簇中提取节点对应的新闻正文使用
    :param corpus_path: 语料的路径
    :return: dict, {news_id: news}
    """
    news_dict = {}
    for line in open(corpus_path):
        line = line.strip().split('\t')
        if len(line) == 3:
            news_id = line[0]
            word_list = line[2]
            news_dict[news_id] = word_list
    return news_dict


def get_event_news(text_dict, node_list):
    """
    从text_dict中提取node_list里面所有的对应的新闻或者新闻标题内容
    :param text_dict:dict: {news_id: news_title+content}
    :param node_list: list: [news_id]
    :return: list: [news_title+content]
    """
    # 读取文章中的内容
    text_list = []
    for node in node_list:
        text_list.append(text_dict.get(str(node)))

    return text_list


def load_data_test():
    dp, dict_init, stop_words = data_process.DataPressing(), dicts.init(), load_stop_words()
    # 分词
    tk = tokenization.Tokenizer(dp, dict_init, stop_words)
    # 获取三张表中的所有新闻
    df_result = get_data()
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


def trans_df_data(df_result):
    """
    提取dataFrame中的标题和正文数据，然后对数据进行分词等预处理之后，并且计算每篇文本的ifidf值。
    :param df_result:
    :return:
    """
    dp, dict_init, stop_words = data_process.DataPressing(), dicts.init(), tokenization.load_stop_words()
    tk = tokenization.Tokenizer(dp, dict_init, stop_words)
    res_lists = []
    for i in range(len(df_result)):
        news_id = df_result.iloc[i]['id']
        title = df_result.iloc[i]['title']
        content = df_result.iloc[i]['content']
        unix_time = df_result.iloc[i]['unix_time']
        if content and title:
            title = title.strip()
            string = title.strip() + content.strip()
            string_list = tk.token(string)  # 分词
            string = " ".join(item for item in string_list)  # 组合成计算tfidf的输入格式
            text_vector = tfidf.load_tfidf_vectorizer([string]).toarray().reshape(-1)
            if not dp.useless_filter(string_list, dicts.stock_dict):
                # string_list = keywords_extractor.parallel_test(string_list)
                res_lists.append((news_id, string, text_vector, unix_time, title))  # 根据上面的具体格式，组成tuple
                # res_lists.append((string, unix_time))  # 根据上面的具体格式，组合成tuple
    print "length of res_lists: %s" % len(res_lists)
    return res_lists


def data_save():
    """
    读取数据库中的内容，文本预处理之后，保存成本地，用于词向量训练，关键词提取等操作
    :return:
    """
    dp, dict_init, stop_words = data_process.DataPressing(), dicts.init(), load_stop_words()
    tk = tokenization.Tokenizer(dp, dict_init, stop_words)  # 分词
    df_result = get_data()
    # df_result.ix[:, ["content"]].apply(tk.token)
    # 提取dataFrame中的title和content的内容，然后分别进行预处理，

    # 方式一、标题和正文保存为同一个新闻，且新闻标题和正文同时存在
    res_lists = []
    for i in range(len(df_result)):
        news_id = df_result.iloc[i]['id']
        title = df_result.iloc[i]['title']
        content = df_result.iloc[i]['content']
        unix_time = df_result.iloc[i]['unix_time']
        if content and title:
            news_id = news_id.strip()
            title = title.strip()
            string = title.strip() + content.strip()
            string_list = tk.token(string)
            if not dp.useless_filter(string_list, dicts.stock_dict):
                # string_list = keywords_extractor.parallel_test(string_list)  # 提取关键词
                res_lists.append((news_id, title, string_list, unix_time))  # 根据上面的具体格式，组成tuple
                # res_lists.append((string, unix_time))  # 根据上面的具体格式，组合成tuple
    print "length of res_lists: %s" % len(res_lists)
    # 数据更新
    # file_out = open("./data/text_full_index.txt", "w")
    file_out = open(conf.corpus_news, "w")
    for index, content in enumerate(res_lists):
        item = " ".join(item for item in content[2])
        file_out.write(str(content[0]) + "\t" + str(content[3]) + "\t" + item.encode("utf8") + "\n")
    file_out.close()

    # file_out = open("./data/text_title_index.txt", "w")
    file_out = open(conf.corpus_news_title, "w")
    for index, content in enumerate(res_lists):
        file_out.write(str(content[0]) + "\t" + str(content[3]) + "\t" + content[1] + "\n")
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
    # import time
    #
    # now = int(time.time())
    # print now - 60 * 12 * 60 * 60
    # print time_util.timestamp_to_time(now)
    # print time_util.timestamp_to_time(now - 60 * 12 * 60 * 60)
    # # 读取指定时间戳之后的新闻
    # df_result = get_ordered_data(now - 60 * 12 * 60 * 60)
    # print df_result
