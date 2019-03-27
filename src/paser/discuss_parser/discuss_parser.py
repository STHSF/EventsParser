#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: discuss_parser.py
@time: 2019-03-26 22:51
# 识别评论中的股票实体。
# 对讨论进行分词,然后提取评论中的股票实体。
"""
import os
import glob
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing
from src.configure import conf
from src.utils import data_source, log_util, time_util, dicts
from src.utils.data_process import DataPressing
from src.utils.tokenization import Tokenizer, load_stop_words


class DiscussParser(object):
    def __init__(self):
        # 数据处理模块
        self.data_process = DataPressing()
        # 停用词
        self.stop_words = load_stop_words()
        # 股票-股票代码对, 并且对股票代码做一些变换，比如
        _, self.stocks_df = dicts.load_stock_data()

    def cut_process(self, text):
        """
        数据处理模块, 分词、提取股票实体词
        :param text:
        :return:
        """
        # 分词
        # 用到多进程处理dataframe，所以将类申明放到每个进程中，不然在调用token的时候，每个子进程不能再调用初始化词典
        tokenizer = Tokenizer(self.data_process, self.stop_words)
        text_list = tokenizer.token(text)
        # 提取text中涉及到的股票实体，并且转换成股票代码
        stock_list = self.data_process.find_stocks(text_list, self.stocks_df)
        # stock_list = ','.join(stock_list)  # 展示使用
        del tokenizer
        return stock_list

    def tmp_func(self, df):
        """
        apply函数封装
        :param df:
        :return:
        """
        df['stock_list'] = df['text'].apply(self.cut_process)
        # return df[['xid', 'uid', 'stock_list', 'unix_time', 'information_dic']]
        return df

    def apply_parallel(self, df_grouped, func):
        """
        # 多进程处理dataframe
        :param df_grouped:
        :param func:
        :return:
        """
        ret_lst = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(func)(group) for name, group in df_grouped)

        return pd.concat(ret_lst)

    def run(self, target_df):
        """
        多进程处理主程序
        :param target_df:
        :return:
        """
        # 将输入数据按照
        df_grouped = target_df.groupby(target_df.index)
        res = self.apply_parallel(df_grouped, self.tmp_func)
        return res


def read_csv():
    path = '/Users/li/Desktop/sets1'
    file_list = glob.glob(os.path.join(path, "*.csv"))
    data_list = []
    for f in file_list:
        data_list.append(pd.read_csv(f, header=0,
                                     names=[u'create_at', u'desc', u'id', u'rcreate_at', u'rdesc', u'rid', u'rtitle',
                                            u'ruid', u'screen_sname', u'uid'], encoding='utf-8'))
        # data_list.append(pd.read_csv(f))

    df_result = pd.concat(data_list, sort=True)
    print(len(df_result))
    return df_result


def create_dic(df, xid, unix_time):
    tmp = dict()
    tmp['xid'] = df[xid]
    tmp['unix_time'] = df[unix_time]
    # return str(tmp
    return [df[xid], df[unix_time]]


if __name__ == '__main__':
    discuss_parser = DiscussParser()

    test_df = pd.DataFrame()
    target_df = read_csv()
    # 测试用
    target_df = target_df.head(5)
    # 可以优化
    funccc = lambda x: str(x)  # 类型转换
    test_df['xid'] = target_df['id'].apply(funccc)
    test_df['uid'] = target_df['uid'].apply(funccc)
    # 转换时间格式
    test_df['unix_time'] = target_df['create_at'].apply(time_util.timestamp_to_time, style='%Y-%m-%d')
    # 将id和unix_time构建成一个整体
    test_df['information_dic'] = test_df[['xid', 'unix_time']].apply(create_dic, axis=1, args=('xid', 'unix_time'))

    # desc和rdesc两个讨论合并在一起处理
    funcc = lambda x: str(x[0]) + '.' + str(x[1])
    test_df['text'] = target_df[['desc', 'rdesc']].apply(funcc, axis=1)

    res = discuss_parser.run(test_df)
