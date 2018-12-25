#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: tt.py
@time: 2018-12-21 11:15
"""
import pandas as pd
import numpy as np

# 分组 - 可迭代的对象
df = pd.DataFrame({'X': ['A', 'B', 'A', 'B'], 'Y': [1, 3, 4, 2]})
print(df)
print(df.groupby('X'), type(df.groupby('X')))
print('-------')
print(list(df.groupby('X')), '->可迭代对象，直接生成list\n')
print(list(df.groupby('X'))[0], '->以元组的形式显示')
for n, g in df.groupby('X'):
    print(n)
    print(g)
    print('###')
print('--------')
# n是组名，g是分组后的DataFrame
print(df.groupby(['X']).get_group('A'), '\n')
print(df.groupby(['X']).get_group('B'), '\n')
# .get_group提取分组后的组

grouped = df.groupby(['X'])
print(grouped.groups)
print(grouped.groups['A'])  # 也可写 df.groupby('X').groups['A']
print('-------')
# .groups：将分组后的groups转化为dict
# 可以字典索引方法来查看groups里的元素
