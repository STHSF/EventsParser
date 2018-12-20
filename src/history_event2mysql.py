#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: history_event2mysql.py
@time: 2018-12-17 13:53
将更新好的事件按固定格式保存到mysql中
"""

import json
import pandas as pd
import data_reader
from configure import conf
from utils import my_util, event_util
from utils import data_source

event_save_path = conf.event_save_path
# event_save_path = "/Users/li/PycharmProjects/event_parser/src/model/event_model/"

# 从文件目录中导入最新的更新文件
file_new = my_util.find_newest_file(event_save_path)
new_event_units = event_util.load_history_event(file_new)

# 从数据库中读取新闻的id，title，url和timestamp
total_data = data_reader.get_all_data()
# 将id设为index，方面后面根据id提取title和url
total_data_df = total_data.set_index('id')

# 将事件单元的信息整理成规定格式
result = []
for item in new_event_units:
    print '[Info event ID]: %s' % item.event_id
    print '[Info event title]: %s' % item.topic_title
    event_stock = ','.join(k for k in set(item.stocks))
    print '[Info stock]: %s\n' % event_stock
    print '[Info node list]: %s' % item.node_list
    # 从dataFrame中获取事件单元中node的标题和出处
    title_url = []
    time_list = []
    for node_id in item.node_list:
        title, url, unix_time = total_data_df.loc[node_id][['title', 'url', 'unix_time']]
        time_list.append(unix_time)
        title_url.append({node_id: {'news_title': title.encode('utf-8'), 'url': url, 'unix_time': unix_time}})
    event_detail = json.dumps(title_url)
    stop_time = max(time_list)
    start_time = min(time_list)
    print "[Info event time]start_time {}, stop_time {}".format(start_time, stop_time)
    result.append((item.event_id, item.topic_title, event_stock, start_time, stop_time, event_detail))

# 整理成dataFrame的格式
result_df = pd.DataFrame(result, columns=['event_id', 'event_title', 'event_stock', 'start_time', 'stop_time', 'event_detail'])
# 创建数据库引擎
engine_mysql = data_source.GetDataEngine("XAVIER_DB")
# 将整理好的数据保存到mysql中
result_df.to_sql('event_detail', engine_mysql, if_exists='replace')
