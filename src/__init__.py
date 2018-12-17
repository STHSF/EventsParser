#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: __init__.py.py
@time: 2018/10/30 10:44 AM
"""

import time
from src.configure import conf
from src.utils import my_util, event_util
import data_reader
import pandas as pd
import numpy as np

event_save_name = int(time.time())
event_save_path = conf.event_save_path
# event_save_path = "/Users/li/PycharmProjects/event_parser/src/model/event_model/"
# event_util.event_save(new_event_units, event_save_name, event_save_path)

#
file_new = my_util.find_newest_file(event_save_path)
print file_new
new_event_units = event_util.load_history_event(file_new)

for i in new_event_units:
    print i.topic_title
    print i.event_id
    print i.node_list