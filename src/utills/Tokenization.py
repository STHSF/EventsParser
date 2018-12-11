#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: tokenization.py
@time: 2018/11/2 10:40 AM
分词模块
调用jieba分词，添加用户自定义词典，封装，并且去停用词等操作
"""
import sys
import dicts
import codecs
import my_util
import logging.handlers
import jieba.posseg as pseg
from src.utills import data_process
from src.configure import Configure

LOG_FILE = '../log/tokenization.log'
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

stopwords = globals()


def load_stop_words():
    # 停用词库准备, 构建停用词表
    conf = Configure()
    stop_words_path = conf.stop_words_path
    try:
        stop_word = codecs.open(stop_words_path, 'r', encoding='utf8').readlines()
        stop_words = [w.strip() for w in stop_word]
        print("[Info] Stopwords 导入成功！")
        return stop_words
    except BaseException as e:
        print('[Exception] Stop Words Exception: {0}'.format(e))


class Tokenizer(object):
    def __init__(self, data_process, dict_init, stop_words):
        self.data_precessing = data_process
        self.dicts = dict_init  # 初始化人工词典
        # 按照词性去停用词
        self.stop_flag = ['x', 'c', 'u', 'd', 'p', 't',
                          'uj', 'm', 'f',
                          'r']  # 去停用词的词性列表，包括[标点符号、连词、助词、副词、介词、时语素、‘的’, 数词, 方位词, 代词, 形容词, 动词],暂时没有使用，原因是添加的新词没有添加词性，所以新词词性有问题。
        self.stopwords = stop_words

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


def d_test():
    data_processing = data_process.DataPressing()
    dict_init = dicts.init()
    stop_words = load_stop_words()
    tk = Tokenizer(data_processing, dict_init, stop_words)
    # print(["大智慧".decode("utf8")])
    print(["【今日题材】".decode("utf8")])
    print(["关注同".decode("utf-8")])

    # 剔除杂质词
    print(
        data_processing.no_remove("【今日题材】[AI决策]大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，还是注册制的, 关注同花顺财经（ths58）， 获取更多机会。"))
    # 判断content中是否存在某些特殊词
    print(data_processing.useless_remove("[AI决策]大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，还是注册制的"))

    # 对content中的内容进行去停，去杂质词，分词
    # result = tk.token("【今日题材】[AI决策]加多宝的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，还是注册制的")
    result = tk.token("加多宝重推红罐 是否能再与王老吉争锋")
    print('Type of result： {}。'.format(type(result)))
    for i in result:
        print(i)


def paralize_test(text, dataprocess, dict_init, stop_words):
    t = Tokenizer(dataprocess, dict_init, stop_words)
    restult = t.token(text)
    return restult


def multi_token_test():
    """
    多进程测试
    :return:
    """
    import time
    from multiprocessing import Pool
    import multiprocessing as mp

    s = '程序员(英文Programmer)是从事程序开发、维护的专业人员。' \
        '一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，' \
        '特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。'

    dataprocess = data_process.DataPressing()
    dict_init = dicts.init()
    stop_words = load_stop_words()
    # 串行处理
    t0 = time.time()
    res1_l = []
    for i in range(10000):
        res1 = paralize_test(s, dataprocess, dict_init, stop_words)
        res1_l.append(res1)
    print("串行处理花费时间{t}s".format(t=time.time() - t0))

    # 并行处理
    t1 = time.time()
    res2_l = []
    pool = Pool(processes=int(mp.cpu_count() * 0.8))
    for i in range(10000):
        res = pool.apply_async(paralize_test, ((s, dataprocess, dict_init, stop_words),))
        res2_l.append(res)
    # 获取数据
    # for k in res2_l:
    #     print k.get()
    pool.close()
    pool.join()
    print("并行处理花费时间{t}s".format(t=time.time() - t1))


# tokenizer = Tokenizer()
if __name__ == '__main__':
    d_test()
    # multi_token_test()
