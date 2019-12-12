#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: xueqiu_dicsuss_batch.py
@time: 2019-03-29 14:05
"""
import gc
import os
import glob
import pandas as pd
from datetime import datetime, timedelta
from src.utils import time_util, dicts
from src.utils.log import log_util

from src.utils.data_process import DataPressing
from src.utils.tokenization import Tokenizer, load_stop_words

logging = log_util.Logger('xueqiu_discuss_batch')


# 使用desc和rdesc作为当前用户的讨论数据，用户id为当前用户id，讨论id为
def read_csv(path=None):
    """
    读取原始csv文件
    :param path:
    :return:
    """
    if path is None:
        path = '/Users/li/Desktop/sets1'
    file_list = glob.glob(os.path.join(path, "*.csv"))
    data_list = []
    for f in file_list:
        data_list.append(pd.read_csv(f, header=0,
                                     names=[u'create_at', u'desc', u'id', u'rcreate_at', u'rdesc', u'rid', u'rtitle',
                                            u'ruid', u'screen_sname', u'uid'], dtype={u'id': str, u'uid': str},
                                     encoding='utf-8'))
        # data_list.append(pd.read_csv(f))

    df_result = pd.concat(data_list, sort=True)

    return df_result


def create_dic(df, xid, unix_time):
    """
    将xid和unix_time构建成一个list
    :param df:
    :param xid:
    :param unix_time:
    :return:
    """
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


def cut_process(text, data_process, tokenizer, stocks_df):
    text_list = tokenizer.token(text)
    # 提取text中涉及到的股票实体，并且转换成股票代码
    stock_list = data_process.find_stocks(text_list, stocks_df)
    del data_process, tokenizer
    gc.collect()
    logging.logger.info("__cut_process ing")
    return stock_list


def discuss_batch(discuss_df, data_process, tokenizer, stocks_df):
    # 对讨论数据做分词并提取股票列表
    discuss_df['stock_list'] = discuss_df['text'].apply(cut_process, args=(data_process, tokenizer, stocks_df))

    # 对result_df下的文章id和股票集合进行结构调整
    # 可以改进成直接调用transform_fuc
    apply_func = lambda x: transform_fuc(x[0], x[1])
    discuss_df['transform_res'] = discuss_df[['xid', 'stock_list']].apply(apply_func, axis=1)
    # print(result_df['transform_res'])

    # 将若干个list合并成一个list
    transform_res_list = []
    for i in discuss_df['transform_res'].values:
        transform_res_list += i

    # 转换成DataFrame格式
    transform_res_df = pd.DataFrame(transform_res_list, columns=['stock', 'xid'])

    # 将数据根据股票分组
    transform_res_grouped = transform_res_df.groupby('stock')

    # 合并每个分组中的文章id
    res_grouped = []
    for group_index, group_df in transform_res_grouped:
        res_grouped.append([group_index, ','.join(group_df['xid'])])
    # print(res_grouped)

    # 构建成dataFrame格式，结合运行日期，保存到数据库中
    batch_result = pd.DataFrame(res_grouped, columns=['stock', 'xid_list'])

    logging.logger.info("length of batch_result: %s" % len(batch_result))
    del transform_res_df, transform_res_grouped, discuss_df
    gc.collect()
    return batch_result


if __name__ == '__main__':
    st_time = datetime.now()

    # 解析器所需要的数据初始化
    stop_words = load_stop_words()
    _, stocks_df = dicts.load_stock_data()
    data_process = DataPressing()
    tokenizer = Tokenizer(data_process, stop_words)

    # 新建空df用于存放预处理的数据
    test_df = pd.DataFrame()
    # 读取数据
    target_df = read_csv()
    logging.logger.info('length of target from csv:{}'.format(len(target_df)))
    # 测试用
    target_df = target_df.head(500)
    # 可以优化， 在read_csv中添加dtype
    # funccc = lambda x: str(x)  # 类型转换
    # test_df['xid'] = target_df['id'].apply(funccc)
    # test_df['uid'] = target_df['uid'].apply(funccc)
    test_df['xid'] = target_df['id']
    # 转换时间格式
    test_df['unix_time'] = target_df['create_at'].apply(time_util.timestamp_to_time, style='%Y-%m-%d')
    # 将id和unix_time构建成一个整体
    test_df['information_dic'] = test_df[['xid', 'unix_time']].apply(create_dic, axis=1, args=('xid', 'unix_time'))

    # desc和rdesc两个讨论合并在一起处理
    funcc = lambda x: str(x[0]) + '.' + str(x[1])
    test_df['text'] = target_df[['desc', 'rdesc']].apply(funcc, axis=1)

    test_df['unix_time'] = target_df['create_at'].apply(time_util.timestamp_to_time, style='%Y-%m-%d')
    # print(test_df[['unix_time', 'xid', 'text']])
    del target_df
    gc.collect()

    # 获取时间的最大值和最小值
    # start_date = time_util.timestamp_to_time(target_df['create_at'].min(), style='%Y-%m-%d')
    # stop_date = time_util.timestamp_to_time(target_df['create_at'].max(), style='%Y-%m-%d')
    # 获取时间的最大值和最小值
    start_date = test_df['unix_time'].min()
    stop_date = test_df['unix_time'].max()
    logging.logger.info('start_time: {}, stop_time: {}'.format(start_date, stop_date))

    start_time = datetime.strptime(str(start_date), "%Y-%m-%d")
    stop_time = datetime.strptime(str(stop_date), "%Y-%m-%d")
    tmp_time = stop_time
    while tmp_time >= start_time:
        # 从最大的一天开始倒数着计算每一天
        # 读取当天的数据
        tmp_date = datetime.strftime(tmp_time, "%Y-%m-%d")
        discuss_df = test_df.loc[test_df['unix_time'] == tmp_date]
        if len(discuss_df) == 0:
            logging.logger.warning("{} has no discuss data".format(tmp_date))
            tmp_time = tmp_time - timedelta(days=1)
            continue
        logging.logger.info("computing {} data at ".format(len(discuss_df), tmp_date))
        # 单进程调用解析器
        result = discuss_batch(discuss_df, data_process, tokenizer, stocks_df)
        result['created_date'] = tmp_date
        logging.logger.info("{} has {} result data".format(tmp_date, len(result)))

        # # 创建数据库引擎
        # engine_mysql_test = data_source.GetDataEngine("XAVIER_DB")
        # engine_mysql = data_source.GetDataEngine("XAVIER")
        # result.to_sql('history_discuss_filter', engine_mysql, if_exists='append', index=False)
        # engine_sqlite = data_source.GetDataEngine('XAVIER_SQLITE')
        # result.to_sql('history_discuss_filter', engine_sqlite, if_exists='append', index=False)

        # 计算前一天时间
        del result, discuss_df
        gc.collect()
        tmp_time = tmp_time - timedelta(days=1)

    end_time = datetime.now()
    print((end_time - st_time).seconds)




