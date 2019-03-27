#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: xueqiu_discuss_daily_bak.py
@time: 2019-03-18 16:35
对大V评论进行分析，提取大V评论中的股票实体，并且整合成股票ID:{评论ID, 评论大VID, 评论时间, 评论内容}
计算时间粒度，一天
每天定时统计, 每天早上八点定时运行
"""

import datetime
from src.utils import dicts, time_util
import pandas as pd
from src.data_reader import read_all_data
from src.utils import log_util, dicts
from src.paser.discuss_parser import discuss_parser

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

    xq_parser = discuss_parser.DiscussParser()

    # 获取两个指定的时间点
    # 起始时间
    stop_time = time_util.get_integral_point_time(9)
    # 截止时间为起始时间的前一天
    start_time = time_util.get_integral_point_time(9) - 86400  # (24*60*60)

    # 测试用
    start_time = 1552179600
    stop_time = 1552179600 + 86400

    logging.logger.info("program start at {}".format(start_time))
    # 读取原始雪球评论数据
    sheet_name = 'xueqiu_discuss'
    sql = "SELECT xid, uid, title, text, unix_time FROM xavier.{} WHERE unix_time >={} AND unix_time <= {} order by unix_time".format(sheet_name, str(start_time), str(stop_time))
    # sql = "SELECT count(*) FROM xavier_db.%s  ORDER BY unix_time" % sheet_name

    # 读取需要处理的数据，从数据库中以DataFrame的格式读取。
    discuss_df = read_all_data(sheet_name, sql)
    # 测试用
    discuss_df = discuss_df.head()
    if len(discuss_df) <= 0:
        logging.logger.warning('there is no new discuss yesterday')
        exit()
    else:
        logging.logger.info('load discuss data from mysql successful')

    # print('discuss_df %s' % discuss_df)
    result_df = xq_parser.run(discuss_df)

    # 对result_df下的文章id和股票集合进行结构调整
    # 可以改进成直接调用transform_fuc
    apply_func = lambda x: transform_fuc(x[0], x[1])
    result_df['transform_res'] = result_df[['xid', 'stock_list']].apply(apply_func, axis=1)
    print(result_df['transform_res'])

    # 将若干个list合并成一个list
    transform_res_list = []
    for i in result_df['transform_res'].values:
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
    result = pd.DataFrame(res_grouped, columns=['stock', 'xid_list'])

    result['created_date'] = str(datetime.date.today().strftime("%Y-%m-%d"))
    print(result)
    logging.logger.info("length of result: %s" % len(result))


    # # 存储到表中
    # # 创建数据库引擎
    # engine_mysql_test = data_source.GetDataEngine("XAVIER_DB")
    # engine_mysql = data_source.GetDataEngine("XAVIER")
    # result.to_sql('discuss_stock_filter_lists', engine_mysql, if_exists='replace', index=False)
    #
    logging.logger.info('program finished')


