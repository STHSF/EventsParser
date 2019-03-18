#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: event2mysql.py
@time: 2018-12-17 13:53
将更新好的事件按固定格式保存到mysql中
"""

import json
import pandas as pd
import data_reader
from configure import conf
from src.utils import file_util, event_util, log_util
from src.utils import data_source

logging = log_util.Logger('event2mysql')
event_save_path = conf.event_save_path
# event_save_path = "/Users/li/PycharmProjects/event_parser/src/model/event_model/"

# 从文件目录中导入最新的更新文件
file_new = file_util.find_newest_file(event_save_path)
new_event_units = event_util.load_history_event(event_save_path + file_new)

# 从数据库中读取最新的新闻的id，title，url和timestamp
total_data = data_reader.get_all_data()
# 将id设为index，方面后面根据id提取title和url
total_data_df = total_data.set_index('id')

# 将事件单元的信息整理成规定格式
result = []
for item in new_event_units:
    # 如果是有效事件
    if item.effectiveness == 1:
        logging.logger.info('[effective event ID]: %s' % item.event_id)
        logging.logger.info('[effective event title]: %s' % item.topic_title)
        event_stock = ','.join(k for k in set(item.stocks))
        logging.logger.info('[effective stock]: %s\n' % event_stock)
        logging.logger.info('[effective node list]: %s' % item.node_list)
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
        logging.logger.info("[event start-stop time]start_time {}, stop_time {}".format(start_time, stop_time))
        result.append((item.event_id, item.topic_title.encode('utf-8'), event_stock, start_time, stop_time, event_detail))
    else:
        continue

# 整理成dataFrame的格式
result_df = pd.DataFrame(result,
                         columns=['event_id', 'event_title', 'event_stock', 'start_time', 'stop_time', 'event_detail'])

# # 创建数据库引擎
engine_mysql = data_source.GetDataEngine("XAVIER_DB")
# # 将整理好的数据保存到mysql中
result_df.to_sql('event_detail', engine_mysql, if_exists='replace', index=False)
logging.logger.info('event_detail update success')
# # 整理出股票对应的事件{}
event_symbol = result_df[['event_id', 'event_stock']]
# print event_symbol
lst = {}
for i in range(len(event_symbol)):
    event_id = event_symbol.loc[i]['event_id']
    event_stock = event_symbol.loc[i]['event_stock'].strip()
    # if event_stock != '':   # 剔除没有股票的事件
    #     for symbol in event_stock.split(','):
    #         lst.setdefault(symbol, []).append("'" + str(event_id) + "'")
    for symbol in event_stock.split(','):
        lst.setdefault(symbol, []).append("'" + str(event_id) + "'")

tmp_result = pd.DataFrame(list(lst.items()), columns=['SYMBOL', 'event_id'])
tmp_result['event_id'] = tmp_result['event_id'].apply(lambda x: ','.join(x))
# print tmp_result
# 将整理好的数据保存到mysql中
tmp_result.to_sql('symbol_event_detail', engine_mysql, if_exists='replace', index=False)
logging.logger.info('symbol_event_detail update success')
