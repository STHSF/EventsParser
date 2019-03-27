#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: xueqiu_discuss_csv.py
@time: 2019-03-23 14:23
"""

# 从csv文件中读取文件
import time
import os
import glob
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing
from src.configure import conf
from src.utils import data_source, log_util, time_util, dicts
from src.utils.data_process import DataPressing
from src.utils.tokenization import Tokenizer, load_stop_words
from src.paser.discuss_parser import discuss_parser


logging = log_util.Logger('xueqiu_discuss_csv')


# 使用desc和rdesc作为当前用户的讨论数据，用户id为当前用户id，讨论id为
def read_csv(path=None):
    if path is None:
        path = '/Users/li/Desktop/sets1'
    file_list = glob.glob(os.path.join(path, "*.csv"))
    data_list = []
    for f in file_list:
        data_list.append(pd.read_csv(f, header=0,
                                     names=[u'create_at', u'desc', u'id', u'rcreate_at', u'rdesc', u'rid', u'rtitle',
                                            u'ruid', u'screen_sname', u'uid'], encoding='utf-8'))
        # data_list.append(pd.read_csv(f))

    df_result = pd.concat(data_list, sort=True)

    return df_result


def create_dic(df, xid, unix_time):
    tmp = dict()
    tmp['xid'] = df[xid]
    tmp['unix_time'] = df[unix_time]
    return [df[xid], df[unix_time]]


# 数据结构调整
def transform_fuc(id, stock_list):
    """
    将user_id和stock_list两两组合成tuple的list集合
    :param id: str
    :param stock_list: list
    :return:
    """
    if len(stock_list) <= 0:
        pass
    user_id_list = [id] * len(stock_list)
    tuple_zip = zip(stock_list, user_id_list)
    tuple_list = list(tuple_zip)
    return tuple_list


if __name__ == '__main__':
    start_time = time.time()
    xq_discuss_parser = discuss_parser.DiscussParser()

    test_df = pd.DataFrame()
    target_df = read_csv()
    logging.logger.info('length of target from csv:{}'.format(len(target_df)))
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

    # 提取股票实体词
    result_df = xq_discuss_parser.run(test_df)
    # print(result_df[['stock_list', 'information_dic']])

    # 对result_df下的文章id和股票集合进行结构调整
    apply_func = lambda x: transform_fuc(x[0], x[1])
    result_df['transform_res'] = result_df[['information_dic', 'stock_list']].apply(apply_func, axis=1)
    # print(result_df['transform_res'])
    # print(result_df['transform_res'])

    # 将若干个list合并成一个list
    transform_res_list = []
    for i in result_df['transform_res'].values:
        transform_res_list += i

    # 转换成DataFrame格式
    transform_res_df = pd.DataFrame(transform_res_list, columns=['stock', 'information_list'])
    # print(transform_res_df[['stock', 'information_list']])
    # 将数据根据股票分组
    transform_res_grouped = transform_res_df.groupby('stock')

    # 合并每个分组中的文章id
    res_grouped = []
    for group_index, group_value in transform_res_grouped:
        if group_index is None or group_index:
            pass
        tmp_res = []
        for value in group_value['information_list']:
            tmp_res.append(value)
        res_grouped.append([group_index, tmp_res])

    # 构建成dataFrame格式，结合运行日期，保存到数据库中
    result = pd.DataFrame(res_grouped, columns=['stock', 'information_list'])
    # print("result %s" % result)

    result_dataframe = pd.DataFrame()
    for i, j in result.iterrows():
        tt = pd.DataFrame(j['information_list'], columns=['xid', 'created_time'])
        # print('tt %s' % tt)
        tt_grouped = tt.groupby('created_time')

        # 合并每个分组中的文章id
        res_grouped = []
        for i1, j1 in tt_grouped:
            # print('i1 %s' % i1)
            # print('j1 %s' % j1)
            res_grouped.append([i1, ','.join(j1['xid'])])
        # print(res_grouped)

        result_df = pd.DataFrame(res_grouped, columns=['creates_time', 'xid_list'])
        result_df['stock'] = j['stock']

        # print(result_df)
        result_dataframe = result_dataframe.append(result_df, ignore_index=True)
    logging.logger.info('spend %s' % (time.time() - start_time))
    logging.logger.info('length of result dataframe:\n %s' % len(result_dataframe))

    # 数据库存储
    # engine_sqlite = data_source.GetDataEngine('XAVIER_SQLITE')
    # engine_mysql = data_source.GetDataEngine("XAVIER")
    #
    # result_dataframe.to_sql('history_discuss_stock_filter', engine_mysql, if_exists='replace', index=False)
    # result_dataframe.to_sql('history_discuss_stock_filter', engine_sqlite, if_exists='replace', index=False)
