#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: dynamic_update.py
@time: 2018/12/5 2:23 PM
增量式事件更新，基于历史事件库，将新增新闻实时与历史事件库进行相似度计算，最后合并
"""
import sys
sys.path.append('../')
sys.path.append('..')
sys.path.append('../../')
import gc  # noqa: E402
import time  # noqa: E402
import datetime  # noqa: E402
import data_reader  # noqa: E402
import pandas as pd  # noqa: E402
from tqdm import tqdm  # noqa: E402
from utils import log  # noqa: E402
from configure import conf  # noqa: E402
from utils import event_util, my_util  # noqa: E402
from cluster.singlePass import singlePassCluster  # noqa: E402


logging = log.Logger('dynamic_update', level='debug')
# step 1、读取指定日期之后的新闻
# 读取当前时间段时间
now = datetime.date.today()
today_timestamp = int(time.mktime(now.timetuple()))
logging.logger.info('读取新闻的起始时间: {}'.format(today_timestamp))
ordered_df = data_reader.get_ordered_data(timestamp=today_timestamp)
# 提取dataFrame中的内容
ordered_news_lists = data_reader.trans_df_data(ordered_df)

# 如果当天没有新闻更新，则直接退出程序，事件单元不需要更新。
if len(ordered_news_lists) <= 0:
    # print '今天没有新新闻，事件单元不更新'
    logging.logger.info('[事件库未更新]: 今天没有新新闻，事件单元不更新')
    sys.exit()

# for tmp in ordered_news_lists:
#     print tmp[0], tmp[1]

# step 2、导入历史事件
history_event_units = event_util.load_history_event()
# print "[Info] 事件库中事件的个数 %s" % len(history_event_units)
logging.logger.info("[事件库中事件的个数:] {}".format(len(history_event_units)))
# for index, event_unit in enumerate(history_event_units):
#     print "cluster: %s" % index  # 簇的序号
#     print event_unit.node_list  # 该簇的节点列表
#     print event_unit.centroid

len_news = len(ordered_news_lists)
new_event_units = []
new_event_units.extend(history_event_units)
# step 3、遍历新新闻，然后将新新闻添加到事件单元中，更新事件单元的节点和簇心
for news_index in tqdm(range(len_news)):  # 遍历每一篇新的新闻
    # 新的节点id
    new_node_id = ordered_news_lists[news_index][0]
    # 新的节点的VSM
    new_node_vec = ordered_news_lists[news_index][2]
    # max_dist = singlePassCluster.cosine_distance(history_event_units[0].centroid, ordered_news_lists[news_index][2])
    max_dist = singlePassCluster.cosine_distance(new_event_units[0].centroid, new_node_vec)
    min_event_index = 0
    for event_index, new_event_unit in enumerate(new_event_units[1:]):  # 遍历每一个事件单元
        # 计算当前新闻和每个事件元之间距离
        # dist = singlePassCluster.cosine_distance(history_event_unit.centroid, ordered_news_lists[news_index][2])
        dist = singlePassCluster.cosine_distance(new_event_unit.centroid, new_node_vec)
        # print 'dist: %s' % dist
        # 找出最大的距离的事件元
        if dist > max_dist:
            max_dist = dist
            min_event_index = event_index + 1
    logging.logger.info('[Info] new_node_id: %s' % new_node_id)
    logging.logger.info('[Info] len of new_event_unit: %s' % len(new_event_units))
    logging.logger.info('[Info] max_dist: %s' % max_dist)
    logging.logger.info('[Info] min_cluster_index: %s\n' % min_event_index)
    # 如果最大距离大于某一个阈值，则将该新闻归并到该事件单元
    if max_dist > 10:
        # new_node_id = ordered_news_lists[news_index][0]
        # new_node_vec = ordered_news_lists[news_index][2]
        new_event_units[min_event_index].add_node(new_node_id, new_node_vec)
        # new_event_units[min_event_index].add_unit_title()
        # new_event_units[min_event_index].event_expression()
    else:
        # 否则则新建一个事件单元
        index = len(new_event_units)
        new_event = event_util.EventUnit()
        new_event.event_id = index
        new_event.add_node(new_node_id, new_node_vec)
        # new_event.add_unit_title()
        # new_event.event_expression()
        new_event_units.append(new_event)
        del new_event
        gc.collect()

logging.logger.info('[更新后的事件个数]: {}'.format(len(new_event_units)))
# step 4、对更新的事件库进行标题和关键词更新
# 事件库更新，更新标题，关键词,股票代码。
# 读取数据库中的所有新闻数据
full_df_data = data_reader.get_all_data().set_index('id')

# 股票及股票代码
stock_df = pd.read_csv(conf.stock_new_path, encoding='utf-8').set_index('SESNAME')

for unit in tqdm(new_event_units):
    if unit.event_tag == 1:
        # 更新标题，股票代码，关键词等
        logging.logger.info("事件 [%s] 是新事件" % unit.event_id)
        # 读取每个事件
        node_df_data = full_df_data.loc[set(unit.node_list)]
        node_news_lists = data_reader.trans_df_data(node_df_data.reset_index())
        news_list = []
        news_title_list = []
        for i in node_news_lists:
            # print i[1], i[4]
            news_list.append(i[1])
            news_title_list.append(i[4])
        # 更新股票列表
        unit.event_expression(news_title_list, news_list, stock_df)
        logging.logger.info("股票列表: %s" % ','.join(tmp for tmp in unit.stocks))
        logging.logger.info("关键词列表: %s" % unit.keywords)
        # 更新标题
        node_news_dict = {}
        for node in node_news_lists:
            node_news_dict[node[0]] = (node[1], node[2], node[3], node[4])
        unit.title_update(node_news_dict)
        unit.event_tag = 0  # 所有内容更新完成之后将事件表示为0
    else:
        continue


# step 5、将更新后的事件单元保存下来
event_save_name = int(time.time())
event_save_path = conf.event_save_path
# event_save_path = "/Users/li/PycharmProjects/event_parser/src/model/event_model/"
event_util.event_save(new_event_units, event_save_name, event_save_path)

# step 6、load最新的事件单元库
file_new = my_util.find_newest_file(event_save_path)
logging.logger.info('[最新的文件: %s]' % file_new)
# new_event_units = event_util.load_history_event(file_new)
# for i in new_event_units:
#     print i.topic_title
#     print i.event_id
#     print i.node_list
#     print i.stocks
