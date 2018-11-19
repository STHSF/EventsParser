#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: Tokenization.py
@time: 2018/11/2 10:40 AM
分词模块
调用jieba分词，添加用户自定义词典，封装，并且去停用词等操作
"""
import sys
sys.path.append("../")
import dicts
import codecs
import my_utils
import logging.handlers
import jieba.posseg as pseg
from DataProcess import DataPressing
from configure import Configure


LOG_FILE = '../log/tokenization.log'
my_utils.check_path(LOG_FILE)
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


stopwords = globals()


class Tokenizer(object):
    def __init__(self):
        self.data_precessing = DataPressing()
        self.dicts = dicts.init()  # 初始化人工词典
        # 按照词性去停用词
        self.stop_flag = ['x', 'c', 'u', 'd', 'p', 't',
                          'uj', 'm', 'f', 'r', 'a', 'v']  # 去停用词的词性列表，包括[标点符号、连词、助词、副词、介词、时语素、‘的’, 数词, 方位词, 代词, 形容词, 动词],暂时没有使用，原因是添加的新词没有添加词性，所以新词词性有问题。

        # 停用词库准备, 构建停用词表
        conf = Configure()
        stop_words_path = conf.stop_words_path
        try:
            stopwords = codecs.open(stop_words_path, 'r', encoding='utf8').readlines()
            self.stopwords = [w.strip() for w in stopwords]
            print("[Info] Stopwords 导入成功！")
        except BaseException as e:
            print('[Exception] Stop Words Exception: {0}'.format(e))

    def token(self, text):
        """
        对语料进行分词，分词之后先按照词性过滤出一些停用词，然后在通过停用词表过滤掉一些停用词。
        :param text:
        :return:
        """
        result = []
        words = pseg.cut(self.data_precessing.no_remove(text))

        for word, flag in words:
            if flag not in self.stop_flag and word not in self.stopwords and len(word) >= 2:
                result.append(word)
        return result


if __name__ == '__main__':
    t = Tokenizer()
    data_processing = DataPressing()
    # print(["大智慧".decode("utf8")])
    print(["【今日题材】".decode("utf8")])
    print(["关注机会。".decode("utf-8")])

    # 剔除杂质词
    print(data_processing.no_remove("【今日题材】[AI决策]大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，还是注册制的, 关注同花顺财经（ths58）， 获取更多机会。"))
    # 判断content中是否存在某些特殊词
    print(data_processing.useless_remove("[AI决策]大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，还是注册制的"))

    # 对content中的内容进行去停，去杂质词，分词
    result = t.token("【今日题材】[AI决策]大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，还是注册制的")
    print('Type of result： {}。'.format(type(result)))
    for i in result:
        print(i)
