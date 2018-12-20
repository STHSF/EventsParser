#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: data_source.py
@time: 2018/10/30 6:39 PM
"""


URL = 'url'
DTYPE = 'DTYPE'
OBJ = 'OBJ'

SQLALCHEMY = 1

__DNS = {
    'DNDS':{
        URL:'mssql+pymssql://reader:reader@10.15.97.127:1433/dnds',
        DTYPE:SQLALCHEMY
    },

    'XAVIER': {
        URL: 'mysql+mysqlconnector://root:t2R7P7@10.15.5.86:3306/xavier',
        DTYPE: SQLALCHEMY
    },
    'XAVIER_DB': {
        URL: 'mysql+mysqlconnector://root:t2R7P7@10.15.5.86:3306/xavier_db',
        DTYPE: SQLALCHEMY
    }
}


def __getSqlAlchemyEngine(source):
    if not OBJ in __DNS[source].keys():
        import sqlalchemy as sa
        __DNS[source][OBJ] = sa.create_engine(__DNS[source][URL])
    return __DNS[source][OBJ]


def GetDataEngine(source):
    engine = None
    if source in __DNS.keys():
        if __DNS[source][DTYPE] == SQLALCHEMY:
            return __getSqlAlchemyEngine(source)
    else:
        raise Exception("未知的数据源 --'{0}'")
    return engine

