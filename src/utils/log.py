#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: log_test.py
@time: 2018-12-26 16:33
"""

import logging
import my_util
from logging import handlers


class Logger(object):
    level_relations = {
        # 读取的事件文件目录
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, log_file_name, level='debug', when='D', backup_count=5,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        log_file = '../log/%s.log' % log_file_name
        my_util.check_path(log_file)
        self.logger = logging.getLogger(log_file)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=log_file, when=when, backupCount=backup_count,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


if __name__ == '__main__':
    log = Logger('all.log', level='info')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning(u'警告')
    log.logger.error(u'报错')
    log.logger.critical(u'严重')
    Logger('error.log', level='error').logger.error('error')
