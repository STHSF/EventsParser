#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: load_event_data.py
@time: 2018-12-25 18:18
"""
from configure import conf
from utils import my_util, event_util


event_save_path = conf.event_save_path
# event_save_path = "/Users/li/PycharmProjects/event_parser/src/model/event_model/"

# 从文件目录中导入最新的更新文件
file_new = my_util.find_newest_file(event_save_path)
new_event_units = event_util.load_history_event(file_new)

for i in new_event_units:
    print "topic_title %s" % i.topic_title
    print "event_id %s" % i.event_id
    print "node_list %s" % i.node_list
    print "stock_list %s\n" % i.stocks
