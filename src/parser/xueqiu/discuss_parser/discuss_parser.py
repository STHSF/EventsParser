#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: 1.0
@author: LiYu
@file: discuss_parser.py
@time: 2019-03-26 22:51
# 识别评论中的股票实体。
# 对讨论进行分词,然后提取评论中的股票实体
# 代码中使用了多进程来处理DataFrame数据。
"""
import os
import glob
import time
import pandas as pd
import multiprocessing
from joblib import Parallel, delayed
from src.utils import dicts
from src.utils.data_process import DataPressing
from src.utils.tokenization import Tokenizer, load_stop_words


class DiscussParser(object):
    """
    讨论解析器
    """
    def __init__(self):
        # 加载分词自定义词典
        dicts.init()
        self.data_process = DataPressing()
        # 停用词
        self.stop_words = load_stop_words()
        # 股票-股票代码对, 并且对股票代码做一些变换，比如
        _, self.stocks_df = dicts.load_stock_data()
        self.tokenizer = Tokenizer(self.data_process, self.stop_words)

    def __cut_process(self, text):
        """
        数据处理模块, 分词、提取股票实体词
        :param text:
        :return:
        """
        print('cut_process进程: %sd   父进程ID：%s' % (os.getpid(), os.getppid()))
        # 分词
        # 用到多进程处理DataFrame，所以将类申明放到每个进程中，不然在调用token的时候，每个子进程不能再调用初始化词典
        text_list = self.tokenizer.token(text)
        # print("text_list %s" % text_list)
        # 提取text中涉及到的股票实体，并且转换成股票代码
        stock_list = self.data_process.find_stocks(text_list, self.stocks_df)
        # stock_list = ','.join(stock_list)  # 展示使用
        return stock_list

    def tmp_func(self, tmp_df, column="text"):
        """
        apply函数封装
        :param column: 需要处理的列名
        :param tmp_df:
        :return:
        """
        print('tmp_func进程: %sd   父进程ID：%s' % (os.getpid(), os.getppid()))
        tmp_df['stock_list'] = tmp_df[column].apply(self.__cut_process)
        return tmp_df

    @staticmethod
    def __apply_parallel(df_grouped, func):
        """
        # 多进程处理dataframe
        :param df_grouped:
        :param func:
        :return:
        """
        print('apply_parallel是进程: %sd   父进程ID：%s' % (os.getpid(), os.getppid()))
        num_cpu = multiprocessing.cpu_count()

        # Parallel不使用参数的时候, 程序多进程运行, 但是字典没有加载
        # res_list = Parallel(n_jobs=num_cpu - 2)(delayed(func)(group) for name, group in df_grouped)
        # 单独使用prefer参数, 依然是单进程
        # res_list = Parallel(n_jobs=num_cpu - 2, prefer="threads")(delayed(func)(group) for name, group in df_grouped)
        # 单独使用backend, 词典可以加载成功
        # res_list = Parallel(n_jobs=num_cpu - 2, backend="multiprocessing")(delayed(func)(group) for name, group in df_grouped)
        # 两个参数都设置, 词典加载成功, 而且运行时间略有缩短
        res_list = Parallel(n_jobs=(num_cpu - 2), backend="multiprocessing", prefer="threads")(delayed(func)(group) for name, group in df_grouped)
        return pd.concat(res_list)

    def run(self, target_df):
        """
        多进程处理主程序
        :param target_df:
        :return:
        """
        # print('run进程: %sd   父进程ID：%s' % (os.getpid(), os.getppid()))
        # 将输入数据按照
        df_grouped = target_df.groupby(target_df.index)
        res_df = self.__apply_parallel(df_grouped, self.tmp_func)
        return res_df


# 测试用接口
def read_csv():
    path = '/Users/li/Desktop/sets1'
    file_list = glob.glob(os.path.join(path, "*.csv"))
    data_list = []
    for f in file_list:
        data_list.append(pd.read_csv(f,
                                     header=0,
                                     names=[u'create_at', u'desc', u'id', u'rcreate_at', u'rdesc',
                                            u'rid', u'rtitle', u'ruid', u'screen_sname', u'uid'], encoding='utf-8'))
        # data_list.append(pd.read_csv(f))

    df_result = pd.concat(data_list, sort=True)
    print(len(df_result))
    return df_result


def create_dic(target_df, xid, unix_time):
    tmp_dic = dict()
    tmp_dic['xid'] = target_df[xid]
    tmp_dic['unix_time'] = target_df[unix_time]
    return [target_df[xid], target_df[unix_time]]


if __name__ == '__main__':

    print('main进程: %sd   父进程ID：%s' % (os.getpid(), os.getppid()))
    discuss_parser = DiscussParser()

    # test_df = pd.DataFrame()
    # target_df = read_csv()
    # # 测试用
    # target_df = target_df.head(5)
    # # 可以优化
    # funccc = lambda x: str(x)  # 类型转换
    # test_df['xid'] = target_df['id'].apply(funccc)
    # test_df['uid'] = target_df['uid'].apply(funccc)
    # # 转换时间格式
    # test_df['unix_time'] = target_df['create_at'].apply(time_util.timestamp_to_time, style='%Y-%m-%d')
    # # 将id和unix_time构建成一个整体
    # test_df['information_dic'] = test_df[['xid', 'unix_time']].apply(create_dic, axis=1, args=('xid', 'unix_time'))
    #
    # # desc和rdesc两个讨论合并在一起处理
    # funcc = lambda x: str(x[0]) + '.' + str(x[1])
    # test_df['text'] = target_df[['desc', 'rdesc']].apply(funcc, axis=1)
    #
    # res = discuss_parser.run(test_df)
    df = pd.DataFrame({'text': ['大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，中信证券不错'] * 1000})
    start_time = time.time()

    res = discuss_parser.run(df)
    print('spend time %s' % (time.time() - start_time))
