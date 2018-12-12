#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: mysql_util.py
@time: 2018/11/28 4:44 PM
"""

import MySqldb
import z


class mysql:
    def __init__(self):
        self.conn = MySqldb.connect(host=z.mysql_ip,
                                    user=z.mysql_user,
                                    passwd=z.mysql_passwd,
                                    db=z.mysql_db,
                                    port=z.mysql_port)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()


ms = mysql()


def load_from_mysql(query_str):
    ms.cursor.execute(query_str)
    result = ms.cursor.fetchall()
    ms.close()
    return result


def insert_data(query_insert):
    # # SQL 插入语句
    # sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
    #          LAST_NAME, AGE, SEX, INCOME)
    #          VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
    try:
        # 执行sql语句
        ms.cursor.execute(query_insert)
        # 提交到数据库执行
        ms.conn.commit()
    except EOFError:
        # Rollback in case there is any error
        ms.conn.rollback()

    # 关闭数据库连接
    ms.close()


def delete_data(query_delete):
    # SQL 删除语句
    # sql = "DELETE FROM EMPLOYEE WHERE AGE > %s" % (20)
    try:
        # 执行SQL语句
        ms.cursor.execute(query_delete)
        # 提交修改
        ms.conn.commit()
    except IOError:
        # 发生错误时回滚
        ms.conn.rollback()

    # 关闭连接
    ms.close()


def update_data(query_update):
    # SQL 更新语句
    # sql = "DELETE FROM EMPLOYEE WHERE AGE > %s" % (20)
    try:
        # 执行SQL语句
        ms.cursor.execute(query_update)
        # 提交修改
        ms.conn.commit()
    except EOFError:
        # 发生错误时回滚
        ms.conn.rollback()

    # 关闭连接
    ms.close()