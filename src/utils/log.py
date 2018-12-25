#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: logging.py
@time: 2018-12-21 17:15
"""
import logging.handlers
import my_util


class LoggerConfig(object):
    def __init__(self, log_file_name):
        self.log_file_name = log_file_name

    def logger_info(self):
        log_file = '../log/%s_info.log' % self.log_file_name
        my_util.check_path(log_file)
        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=10240 * 1024, backupCount=5)  # 实例化handler
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)                 # 实例化formatter
        handler.setFormatter(formatter)               # 为handler添加formatter
        logger = logging.getLogger('info')                 # 获取名为tst的logger
        if not logger.handlers:
            logger.addHandler(handler)  # 为logger添加handler
            logger.setLevel(logging.INFO)
        return logger

    def logger_error(self):
        log_file = '../log/%s_error.log' % self.log_file_name
        my_util.check_path(log_file)
        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=10240 * 1024, backupCount=5)  # 实例化handler
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)                 # 实例化formatter
        handler.setFormatter(formatter)               # 为handler添加formatter
        logger = logging.getLogger('error')                 # 获取名为tst的logger
        if not logger.handlers:
            logger.addHandler(handler)                    # 为logger添加handler
            logger.setLevel(logging.ERROR)
        return logger