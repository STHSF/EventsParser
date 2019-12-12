#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: format_transform.py
@time: 2019-04-09 10:41
数据转换，统计讨论数目
"""
import pandas as pd
from src.utils.engine import data_source


def county(x):
    """
    统计list中元素的个数
    :param x:
    :return:
    """
    tmp = x.split(',')
    return len(tmp)


def symbol_format(x):
    """
    转换股票代码的格式
    :param x:
    :return:
    """
    symbol = x.split('\'')[1]
    head = int(symbol[:1])
    if head == 6 or head == 9:
        return symbol + '.' + 'XSHG'
    elif head == 0 or head == 3 or head == 2:
        return str(symbol) + '.' + 'XSHE'
    elif head == 8 or head == 4:
        return str(symbol) + '.' + 'OC'
    else:
        return str(symbol)


if __name__ == '__main__':

    engine_sqlite = data_source.GetDataEngine("XAVIER_SQLITE")

    sql = "SELECT * FROM history_stock_discuss_filter"
    # sql = "SELECT * FROM history_discuss_stock_filter"
    df = pd.read_sql(sql, engine_sqlite)

    df['symbol'] = df['stock'].apply(symbol_format)

    df['xid_count'] = df['xid_list'].apply(county)

    df_grouped = df.groupby('created_date')

    engine_mysql = data_source.GetDataEngine("VISION")

    for i, j in df_grouped:
        print(len(j))
        # 这边可以统计每天的总讨论数量，由此作为大盘的特征因子
        # 数据按天分批插入数据库，数据如果需要重跑，则需要删掉原始的表
        j.to_sql('history_discuss_stock_filter', engine_mysql, if_exists='append', index=False)


