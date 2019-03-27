#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: __init__.py.py
@time: 2018/10/30 10:44 AM
"""
import sys
sys.path.append('../')
sys.path.append('..')
sys.path.append('../../')
# import pandas as pd
# df = pd.DataFrame({"A":['a','a','b','c','d'],"B":[4,5,6,7,8]}).set_index("A")
# # print df
# kk = ['a', 'b']
# hj = []
# for j in kk:
#     tmp_res = (df.loc[j].values.tolist())
#     if len(tmp_res) > 1:
#         for k in range(len(tmp_res)):
#             hj.extend(tmp_res[k])
#     else:
#         hj.extend(tmp_res)
# print hj


# from collections import Counter
#
# stock_lists = ['a','b','b','b','b','c','c','c','d','d','d','d']
#
# stock_lists_dict = Counter(stock_lists).items()
# stock_lists_dict.sort(key=lambda item: item[1], reverse=True)
#
# stock_list = []
# for i in stock_lists_dict:
#     stock_list.append(i[0])
#
# print stock_list


# import pandas as pd
# # from itertools import groupby #itertool还包含有其他很多函数，比如将多个list联合起来。。
# #
# df = pd.DataFrame({'event_id': [1, 2, 3,4, 5],
#                   'event_stock': [['i1','i2'], ['i3', 'i2'], ['i3', 'i5'], ['i9', 'i7'], ['i9']]})
# print df
#
# lst = {}
#
# for i in range(len(df)):
#     event_id = df.loc[i]['event_id']
#     event_stock = df.loc[i]['event_stock']
#     if len(event_stock) > 0:
#         for symbol in event_stock:
#             lst.setdefault(symbol, []).append(event_id)
#
# print lst

# from collections import defaultdict
# # lst = [{'a': 123}, {'a': 456},{'b': 789}]
#
# dic = {}
# for _ in lst:
#     for k, v in _.items():
#         dic.setdefault(k, []).append(v)
#
# print dic


# from utils import file_util, event_util, time_util
# from configure import conf
# import datetime
# import time
#
# history_event_file = file_util.find_newest_file(conf.event_save_path)
#
# print history_event_file
