#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: Keywords.py
@time: 2018/11/14 8:23 PM
关键词提取程序
"""
import sys
import logging.handlers
import my_util
sys.path.append("../")
from configure import Configure
from pyhanlp import *
from jieba import analyse
from tokenization import Tokenizer

LOG_FILE = '../log/keywords.log'
my_util.check_path(LOG_FILE)
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=1)  # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
# logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(level=logging.INFO)
# logger.setLevel(level=logging.DEBUG)
logger.info("running %s" % ' '.join(sys.argv))


class keywordsExtractor(object):
    def __init__(self):
        conf = Configure()
        self.stopwords_path = conf.stop_words_path
        self.persent = 0.1

    def run(self, document):

        # tk = Tokenizer()
        # document = tk.token(document)
        # 基于Hanlp库的关键词提取
        print("[Info] keywords by Hanlp:")
        keywords_hanlp = HanLP.extractKeyword(document, 20)
        # print ",".join(keyword for keyword in keywords_hanlp)

        # 基于jieba库的关键词抽取
        # 添加停用词
        analyse.set_stop_words(self.stopwords_path)
        # 引入TextRank关键词抽取接口
        textrank = analyse.textrank
        print "[Info] keywords by textrank:"
        # keywords_jieba = textrank(document, 8, allowPOS=['n', 'nr', 'ns', 'vn', 'v'])
        # keywords_jieba = textrank(document, 20, withWeight=True)
        keywords_jieba = textrank(document, 20)
        # 输出抽取出的关键词
        # print ",".join(keyword for keyword in keywords_jieba)

        # 两种关键词提取接口做交集
        print"[Info] 两个关键词提取方法取交集:"
        join_set = set(keywords_hanlp).intersection(set(keywords_jieba))
        # print ",".join(item for item in join_set)
        return join_set


def test():
    # 关键词提取
    document = u"水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，" \
               u"根据刚刚完成了水资源管理制度的考核，有部分省接近了红线的指标，\n" \
               u"有部分省超过红线的指标。对一些超过红线的地方，\n陈明忠表示，对一些取用水项目进行区域的限批，" \
               u"严格地进行水资源论证和取水许可的批准。"

    kex = keywordsExtractor()
    keywords = kex.run(document)
    print ",".join(item for item in keywords)


if __name__ == '__main__':
    test()