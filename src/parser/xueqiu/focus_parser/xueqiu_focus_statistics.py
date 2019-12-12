#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: xueqiu_focus_statistics.py
@time: 2019-04-29 14:47
统计累计大V的股票关注数
"""
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
sys.path.append('../../../../')
sys.path.append('../../../../../')

import pandas as pd
import time
from sqlalchemy import create_engine
from src.utils import time_util
from src.utils.log import log_util
from src.data_reader import read_all_data


logging = log_util.Logger('xueqiu_focus_statistic')


def f(row):
    if row[:2] == 'SH':
        return str(row[2:]) + '.' + 'XSHG'
    elif row[:2] == 'SZ':
        return str(row[2:]) + '.' + 'XSHE'


if __name__ == '__main__':
    pd.set_option('display.max_rows', None, 'display.max_columns', None, "display.max_colwidth", 1000, 'display.width', 1000)
    # engine_mysql_test = data_source.GetDataEngine("VISIONTEST")
    # engine_mysql = data_source.GetDataEngine("VISION")
    engine_mysql_test = create_engine('mysql+mysqlconnector://test_edit:test_edit_2019@db1.irongliang.com:3306/test')

    date_time = time_util.get_integral_point_time(0)
    logging.logger.info("program start at {}".format(time_util.timestamp_to_time(date_time), "%Y-%m-%d"))

    # 读取原始大V关注数据
    # 大V关注所保存的表
    sheet_name = 'xq_user_stock'
    # 读取指定时间段的所有数据
    sql = "SELECT * FROM test.{} WHERE created <={}".format(sheet_name, str(date_time * 1000))

    # 读取需要处理的数据，从数据库中以DataFrame的格式读取。
    focus_df = read_all_data(sheet_name, engine_mysql_test, sql)
    # print(focus_df)
    logging.logger.info("导入 %s 条数据" % len(focus_df))

    res_grouped = []
    focus_grouped = focus_df.groupby('symbol')
    for symbol, value in focus_grouped:
        counts = value['uid'].count()
        res_grouped.append([f(symbol), counts])

    result = pd.DataFrame(res_grouped, columns=['symbol', 'focus_total_count'])
    save_time = date_time - 86400  # (24*60*60)

    result['created_at'] = str(time_util.timestamp_to_time(save_time, "%Y-%m-%d"))

    # 存储到表中
    # 创建数据库引擎
    result.to_sql('xueqiu_focus_total_count', engine_mysql_test, if_exists='append', index=False)
    # print(result)
    logging.logger.info('生成 %s 条数据' % len(result))
    logging.logger.info('数据保存到第 %s 天' % str(time_util.timestamp_to_time(save_time, "%Y-%m-%d")))
    logging.logger.info('program finished, end at %s' % str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))