#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: my_util.py
@time: 2018/11/19 8:52 AM
"""
import os


def check_path(_path):
    """check out weather the _path exists. If not, create a new _path dit"""
    dir_name = os.path.dirname(_path)
    if dir_name:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
