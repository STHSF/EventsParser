#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: __init__.py.py
@time: 2018/10/30 10:44 AM
"""
import data_reader
import pandas as pd
import numpy as np

full_df_data = data_reader.get_data().set_index('id').reset_index()

print full_df_data
# aa = ['11283186','11316681', '605314817', u'10999906']
# print full_df_data.loc[aa]


# dates = pd.date_range('20121001',periods=10)
# df = pd.DataFrame(np.random.randn(10,4) , index = dates,columns=list('abcd'))
#
# print df