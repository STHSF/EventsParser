#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: data_process.py
@time: 2018/10/31 1:32 PM
文本解析类
"""
import re
from src.utills import keywords_extractor, tokenization, dicts


class DataPressing(object):
    def __init__(self):
        # 杂质词
        self.pattern_word = u'(\[AI\u51b3\u7b56\])|(\u3010\u4eca\u65e5\u9898\u6750\u3011)' \
                            u'|(\u5173\u6ce8\u540c.*\u673a\u4f1a\u3002)'
        # [关注同花顺财经(ths518)，获取更多机会。]
        self.pattern_text = u'(\[AI\u51b3\u7b56\])'
        self.num = 4

    def no_remove(self, text):
        """
        杂质词剔除，比如["今日走势", "AI决策"]
        :param text:
        :return:
        """
        result = re.sub(self.pattern_word, "", text.decode('utf8'))
        # result = re.sub(self.pattern_word, "", text)
        return result

    def useless_remove(self, content):
        """
        判断content中是否包含某些字符
        :return:
        """
        matchObj = re.search(self.pattern_text, content.decode('utf8'))
        if matchObj:
            return True
        else:
            return False

    def useless_filter(self, content_list, stock_dicts):
        """
        如果文章中超过5只以上的股票，股市收报类的新闻，则将这篇文章剔除
        :param content_list: 分词之后的文章list
        :param stock_dicts: 股票代码
        :return:
        """
        stock_num = 0
        for item in set(content_list):
            if item in stock_dicts:
                stock_num += 1

        if stock_num >= self.num:
            return True
        else:
            return False

    def find_stocks(self, content_list, stock_dicts):
        """
        提取content_list中所有的股票以及股票代码
        :param content_list: 分词之后的文章list
        :param stock_dicts: 股票代码
        :return: 返回股票列表
        """
        stock_num = []
        for item in set(content_list):
            if item in stock_dicts:
                stock_num.append(item)

        if len(stock_num) > 0:
            return stock_num
        else:
            return []

    def find_keywords(self, content, key1, key2):
        """
        获取一大段文本之间两个关键字之间的内容
        :param content:
        :param key1:
        :param key2:
        :return:
        """
        form = re.compile(key1 + '(.*?)' + key2, re.S)
        result = form.findall(content)
        return result




# dataprocess = DataPressing()

