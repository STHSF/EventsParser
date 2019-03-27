#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: file_util.py
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


def list_all_files(file_path):
    _file = []
    lists = os.listdir(file_path)
    for i in range(len(lists)):
        path = os.path.join(file_path, lists[i])
        if os.path.isdir(path):
            _file.append(list_all_files(path))
        if os.path.isfile(path):
            _file.append(path)

    return _file


def find_newest_file(save_path):
    """
    从文件夹中读取最新保存或修改的文件。
    :param save_path: 目录地址
    :return:
    """
    _file = []
    lists = os.listdir(save_path)  # 列出目录的下所有文件和文件夹保存到lists
    if len(lists) > 0:
        for i in range(len(lists)):
            path = lists[i]
            # 提取文件，剔除文件夹
            if os.path.isfile(save_path + path):
                _file.append(path)
        if len(_file) > 0:
            _file.sort(key=lambda fn: os.path.getmtime(save_path + fn))  # 将文件按时间排序
            file_new = _file[-1]  # 获取最新的文件保存到file_new
            # filetime = datetime.datetime.fromtimestamp(os.path.getmtime(file_new))
        else:
            file_new = 'NULL'
    else:
        file_new = 'NULL'
    # logging.logger.info("文件的最新修改时间：" + filetime.strftime('%Y-%m-%d %H:%M:%S'))
    # logging.logger.info("最新修改的文件(夹)：" + lists[-1])
    return file_new


if __name__ == '__main__':
    print(find_newest_file("/Users/li/PycharmProjects/event_parser/src/model/event_model/"))
    # print list_all_files("/Users/li/PycharmProjects/event_parser/src/log/")
