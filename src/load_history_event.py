#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: load_history_event.py
@time: 2018-12-17 13:53
"""

from src.configure import conf
from src.utils import my_util, event_util

event_save_path = conf.event_save_path
# event_save_path = "/Users/li/PycharmProjects/event_parser/src/model/event_model/"

# load history event unit
file_new = my_util.find_newest_file(event_save_path)
new_event_units = event_util.load_history_event(file_new)

# print event information
for i in new_event_units:
    print '[Info event ID]: %s' % i.event_id
    print '[Info event title]: %s' % i.topic_title
    print '[Info node list]: %s' % i.node_list
    print '[Info stock]: %s\n' % ','.join(k for k in set(i.stocks))
