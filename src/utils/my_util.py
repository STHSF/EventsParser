#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: my_util.py
@time: 2018/11/19 8:52 AM
"""
import os
import datetime


def check_path(_path):
    """check out weather the _path exists. If not, create a new _path dit"""
    dir_name = os.path.dirname(_path)
    if dir_name:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)


def find_newest_file(save_path):
    """
    从文件夹中读取最新的事件单元保存文件。
    :param save_path: 目录地址
    :return:
    """
    lists = os.listdir(save_path)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(save_path + fn))  # 将文件按时间排序
    filetime = datetime.datetime.fromtimestamp(os.path.getmtime(save_path+lists[-1]))
    file_new = os.path.join(save_path, lists[-1])  # 获取最新的文件保存到file_new
    print("[event_util Info] 时间：" + filetime.strftime('%Y-%m-%d %H-%M-%S'))
    print("[event_util Info] 最新修改的文件(夹)：" + lists[-1])
    return file_new
