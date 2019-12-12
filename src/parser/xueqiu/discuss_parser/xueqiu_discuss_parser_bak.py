#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: xueqiu_discuss_parser_bak.py
@time: 2019-03-05 10:31
对大V评论进行分析，提取大V评论中的股票实体，并且整合成股票ID:{评论ID, 评论大VID, 评论时间, 评论内容}
计算时间粒度，一天

"""
from joblib import Parallel, delayed
import multiprocessing
from src.utils import dicts
import pandas as pd
from src.data_reader import read_all_data
from src.configure import conf
from src.utils.engine import data_source
from src.utils.data_process import DataPressing
from src.utils.tokenization import Tokenizer, load_stop_words

# 读取原始雪球评论数据
sheet_name = 'xueqiu_discuss'
sql = "SELECT xid, uid, title, text, mood, unix_time FROM xavier.%s  ORDER BY unix_time" % sheet_name
# sql = "SELECT count(*) FROM xavier_db.%s  ORDER BY unix_time" % sheet_name


# 导入股票实体词
stock_code_dict = []  # 股票代码
stock_dict = []


def load_stock_data():
    dic_path = conf.dic_path
    st_path = dic_path + "/stock_words.txt"
    st_new_path = dic_path + "/stock.csv"
    for st in open(st_path):
        st = st.decode("utf8")
        code1, st_code = st.split("\t")
        code, stock = st_code.split(",")
        stock_code_dict.append(code.strip("\n"))
        stock_dict.append(stock.strip("\n"))

    stocks_df = pd.read_csv(st_new_path, encoding='utf-8')
    # stock_df.append(stocks_df.set_index('SESNAME'))
    for index, row in stocks_df.iterrows():
        stock_dict.append(row.SESNAME)
        stock_dict.append(row.SYMBOL)
    return stock_dict, stocks_df


_, stocks_df = load_stock_data()

# 识别评论中的股票实体。
# 对讨论进行分词,然后提取评论中的股票实体。
data_process = DataPressing()
dict_init = dicts.init()
stop_words = load_stop_words()
tokenizer = Tokenizer(data_process, stop_words)

# 读取需要处理的数据，从数据库中以DataFrame的格式读取。
discuss_df = read_all_data(sheet_name, sql)
# discuss_df = discuss_df.head()
# print('discuss_df %s' % discuss_df['mood'])

# 整理股票代码
stocks_df = stocks_df.set_index('SESNAME')
# print('stocks_df %s' % stocks_df)


def cut_process(text):
    """
    数据处理模块, 分词、提取股票实体词
    :param text:
    :return:
    """
    # 分词
    dicts.init()
    text_list = tokenizer.token(text)
    # 提取text中涉及到的股票实体，并且转换成股票代码
    stock_list = data_process.find_stocks(text_list, stocks_df)
    res = ','.join(stock_list)
    return res


def tmp_func(df):
    """
    apply函数封装
    :param df:
    :return:
    """
    df['stock_list'] = df['text'].apply(cut_process)
    return df[['xid', 'uid', 'mood', 'stock_list', 'unix_time']]


def apply_parallel(df_grouped, func):
    """
    # 多进程处理
    :param df_grouped:
    :param func:
    :return:
    """
    ret_lst = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(func)(group) for name, group in df_grouped)

    return pd.concat(ret_lst)


def run(target_df):
    """
    多进程处理主程序
    :param target_df:
    :return:
    """
    # 将输入数据按照
    df_grouped = target_df.groupby(target_df.index)
    res = apply_parallel(df_grouped, tmp_func)
    return res


def kk_test():
    """
    测试股票实体是否提取成功
    :return:
    """
    text = "大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！中信证券也上市了，还是注册制的, 中信建投也不错。"
    cut_res = cut_process(text)
    print('tmp_res %s' % cut_res)

    test_df = pd.DataFrame({'text': [text, text, text, text, text]})
    # 非多进程下直接提取股票实体
    test_df['stock_list'] = test_df['text'].apply(cut_process)
    print('test_df %s' % test_df)

    # 多进程下提取股票实体
    df_grouped = test_df.groupby(test_df.index)
    pp = apply_parallel(df_grouped, tmp_func)
    print('pp %s' % pp['stock_list'])


# 结构调整
result_df = run(discuss_df)
# 存储到表中
print(result_df.head())

# # 创建数据库引擎
engine_mysql_test = data_source.GetDataEngine("XAVIER_DB")
engine_mysql = data_source.GetDataEngine("XAVIER")

result_df.to_sql('discuss_stock_filter', engine_mysql, if_exists='replace', index=False)

