#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: corpus_update.py
@time: 2018-12-19 16:51
"""
import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('../../../')
import dicts
import jieba
import codecs  # noqa: E402
import pandas as pd  # noqa: E402
from src import data_reader  # noqa: E402
from src.configure import conf  # noqa: E402

reload(sys)
sys.setdefaultencoding('utf-8')


def stock_code_data_process():
    dic_path = conf.dic_path
    stock_new_path = dic_path + "/stock.csv"
    n2_path = dic_path + "/新增2"
    # 处理股票实体
    # 将stock_words.txt中的股票词转换成jieba用户自定义词典的格式，然后添加到jieba的userdict中
    # 读取股票代码
    stock_df = data_reader.read_stock_code('TQ_SK_BASICINFO')
    stock_df['SYMBOL'] = stock_df['SYMBOL'].apply(lambda x: "'" + x + "'")

    stock_dict = []
    for s in stock_df.values:
        code, stock = s[0], s[1]
        stock_dict.append(code + ' ' + '5' + ' ' + 'n')
        stock_dict.append(stock.strip('\n').decode('utf-8') + ' ' + '5' + ' ' + 'n')
    f = codecs.open(n2_path, 'w', 'utf-8')
    for i in stock_dict:
        f.write(i + '\n')  # \n为换行符
    f.close()
    # 数据保存
    stock_df.to_csv(path_or_buf=stock_new_path, index=False)


if __name__ == '__main__':
    stock_code_data_process()
    dic_path = conf.dic_path
    stock_new_path = dic_path + "/stock.csv"
    data_df = pd.read_csv(stock_new_path, encoding="utf-8").set_index('SESNAME')
    print data_df.loc[u'万科A'].values
    # dicts.init()
    # print dicts.stock_dict
    # for index, row in data_df.iterrows():
    #     print row.SESNAME
