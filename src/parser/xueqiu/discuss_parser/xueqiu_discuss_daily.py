#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: xueqiu_discuss_daily.py
@time: 2019-03-18 16:35
对大V评论进行分析，提取大V评论中的股票实体，并且整合成股票ID:{评论ID, 评论大VID, 评论时间, 评论内容}
计算时间粒度，一天
每天定时统计, 每天早上八点定时运行
"""
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
sys.path.append('../../../../')
sys.path.append('../../../../../')

from src.utils import time_util
from src.utils.log import log_util
import pandas as pd
from sqlalchemy import create_engine
from src.data_reader import read_all_data
from src.parser.xueqiu.discuss_parser import discuss_parser, format_transform

logging = log_util.Logger('discuss_stock_filter_daily')


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
    pd.set_option('display.max_rows', None, 'display.max_columns', None, "display.max_colwidth", 1000, 'display.width', 1000)
    # engine_mysql_test = GetDataEngine("VISIONTEST")
    # engine_mysql = data_source.GetDataEngine("VISION")
    engine_mysql_test = create_engine('mysql+mysqlconnector://test_edit:test_edit_2019@db1.irongliang.com:3306/test')

    xq_parser = discuss_parser.DiscussParser()

    '''数据读取部分'''
    '''根据指定的时间格式, 从指定数据库中读取指定表中的数据'''
    # 获取两个指定的时间点
    # 起始时间
    stop_time = time_util.get_integral_point_time(0)
    # 截止时间为起始时间的前一天
    start_time = time_util.get_integral_point_time(0) - 86400  # (24*60*60)

    # 测试用
    # start_time = 1556380800
    # stop_time = 1556380800 + 86400

    logging.logger.info("program start at {}".format(time_util.timestamp_to_time(start_time), "%Y-%m-%d"))
    logging.logger.info("program stop at {}".format(time_util.timestamp_to_time(stop_time), "%Y-%m-%d"))
    # 读取原始雪球评论数据
    # sheet_name = 'xueqiu_discuss'
    # sql = "SELECT xid, uid, title, text, unix_time FROM xavier.{} WHERE unix_time >={} AND unix_time <= {} order by unix_time".format(sheet_name, str(start_time), str(stop_time))
    # 雪球评论所保存的表
    sheet_name = 'xq_comment'
    # 读取指定时间段的所有数据
    sql = "SELECT * FROM test.{} WHERE created_at >={} AND created_at <= {} order by created_at".format(sheet_name, str(start_time * 1000), str(stop_time * 1000))

    # 读取需要处理的数据，从数据库中以DataFrame的格式读取。
    discuss_df = read_all_data(sheet_name, engine_mysql_test, sql)
    # 测试用
    # discuss_df = discuss_df.head()
    # print('discuss_df %s' % discuss_df)
    '''数据读取部分'''

    if len(discuss_df) <= 0:
        logging.logger.warning('there is no new discuss yesterday')
        exit()
    else:
        logging.logger.info('load discuss data from mysql successful')
    # 进行分词，提取股票特征词等操作
    result_df = xq_parser.run(discuss_df)

    # 对result_df下的文章id和股票集合进行结构调整
    # 可以改进成直接调用transform_fuc
    apply_func = lambda x: transform_fuc(str(x[0]), x[1])
    # id: 文章id， stock_list: 提取的的股票集合
    result_df['transform_res'] = result_df[['id', 'stock_list']].apply(apply_func, axis=1)
    # print(result_df['transform_res'])

    # 将dataframe中每一行的若干个list合并成一个list
    transform_res_list = []
    for i in result_df['transform_res'].values:
        transform_res_list += i

    # 转换成DataFrame格式
    transform_res_df = pd.DataFrame(transform_res_list, columns=['stock', 'xid'])
    # print(transform_res_df)

    # # 将数据根据股票分组
    transform_res_grouped = transform_res_df.groupby('stock')
    #
    # 合并每个分组中的文章id
    res_grouped = []
    for stock, group_df in transform_res_grouped:
        res_grouped.append([stock, ','.join(group_df['xid'])])
    # print(res_grouped)

    # # 构建成dataFrame格式，结合运行日期，保存到数据库中
    result = pd.DataFrame(res_grouped, columns=['stock', 'xid_list'])
    # 格式化股票代码
    result['stock'] = result['stock'].apply(format_transform.symbol_format)
    # 统计讨论的数目
    result['xid_count'] = result['xid_list'].apply(format_transform.county)
    # result['created_at'] = str(datetime.date.today().strftime("%Y-%m-%d"))
    result['created_at'] = str(time_util.timestamp_to_time(start_time, "%Y-%m-%d"))

    print(result)
    logging.logger.info("length of result: %s" % len(result))

    # #存储到表中
    # 创建数据库引擎
    result.to_sql('xueqiu_discuss_count', engine_mysql_test, if_exists='append', index=False)
    logging.logger.info('数据保存到第 %s 天' % str(time_util.timestamp_to_time(start_time, "%Y-%m-%d")))

    logging.logger.info('program finished')


