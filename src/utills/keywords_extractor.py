#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: keywords_extractor.py
@time: 2018/11/19 10:19 AM
基于textRank的关键词提取
"""
import sys
import dicts
import my_util
import logging.handlers
import numpy as np
# from operator import itemgetter
import tokenization
from tokenization import load_stop_words
from data_process import DataPressing


LOG_FILE = '../log/keywordsExtractor.log'
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


class TextRank(object):
    def __init__(self, top_k=20, with_weight=False, window=5, alpha=0.85, min_diff=1000):
        """
        :param top_k: return how many top keywords. `None` for all possible words.
        :param with_weight: if True, return a list of (word, weight);
                            if False, return a list of words.
        :param window:
        :param alpha:
        :param min_diff:
        """
        # self.sentence = sentence
        self.word_list = ""
        self.window = window
        self.alpha = alpha
        self.edge_dict = {}  # 记录节点的边连接字典
        self.iter_num = min_diff  # 设置收敛阈值
        self.topK = top_k  # 提取关键词的个数
        self.withWeight = with_weight

    def _cut_sentence(self, sentence):
        """
        # 对句子进行分词
        :return:
        """
        # 使用多进程的时候需要修改一下
        data_process, dict_init, stop_words = DataPressing(), dicts.init(), load_stop_words()
        tk = tokenization.Tokenizer(data_process, dict_init, stop_words)
        self.word_list = tk.token(sentence)
        # dicts.init()
        # jieba.load_userdict('user_dict.txt')
        # tag_filter = ['a', 'd', 'n', 'v']
        # seg_result = pseg.cut(self.sentence)
        # self.word_list = [s.word for s in seg_result if s.flag in tag_filter]
        # print(self.word_list)

    def _create_nodes(self):
        """
        # 根据窗口，构建每个节点的相邻节点,返回边的集合
        :return:
        """
        tmp_list = []
        word_list_len = len(self.word_list)
        for index, word in enumerate(self.word_list):
            if word not in self.edge_dict.keys():
                tmp_list.append(word)
                tmp_set = set()
                left = index - self.window + 1  # 窗口左边界
                right = index + self.window  # 窗口右边界
                if left < 0: left = 0
                if right >= word_list_len: right = word_list_len
                for i in range(left, right):
                    if i == index:
                        continue
                    tmp_set.add(self.word_list[i])
                self.edge_dict[word] = tmp_set

    def _create_matrix(self):
        """
        # 根据边的相连关系，构建矩阵
        :return:
        """
        self.matrix = np.zeros([len(set(self.word_list)), len(set(self.word_list))])
        self.word_index = {}  # 记录词的index
        self.index_dict = {}  # 记录节点index对应的词

        for i, v in enumerate(set(self.word_list)):
            self.word_index[v] = i
            self.index_dict[i] = v
        for key in self.edge_dict.keys():
            for w in self.edge_dict[key]:
                self.matrix[self.word_index[key]][self.word_index[w]] = 1
                self.matrix[self.word_index[w]][self.word_index[key]] = 1
        # 归一化
        for j in range(self.matrix.shape[1]):
            summary = 0
            for i in range(self.matrix.shape[0]):
                summary += self.matrix[i][j]
            for i in range(self.matrix.shape[0]):
                self.matrix[i][j] /= summary

    def _cal_pr(self):
        """
        # 根据textrank公式计算权重
        :return:
        """
        #
        self.PR = np.ones([len(set(self.word_list)), 1])
        for i in range(self.iter_num):
            self.PR = (1 - self.alpha) + self.alpha * np.dot(self.matrix, self.PR)

    def _print_result(self):
        """
        # 输出词和相应的权重
        :return:
        """
        word_pr = {}
        for i in range(len(self.PR)):
            word_pr[self.index_dict[i]] = self.PR[i][0]
        if self.withWeight:
            tags = sorted(word_pr.items(), key=lambda x: x[1], reverse=True)
            # tags = sorted(word_pr.items(), key=itemgetter(1), reverse=True)
        else:
            tags = sorted(word_pr, key=word_pr.__getitem__, reverse=True)

        if self.topK:
            return tags[:self.topK]
        else:
            return tags

    def run(self, sentence):
        if type(sentence) is not list:
            self._cut_sentence(sentence)
        else:
            self.word_list = sentence

        if len(self.word_list) > 1:  # bug 如果sentence分词后只有一个单词，则直接输出
            self._create_nodes()
            self._create_matrix()
            self._cal_pr()
            result = self._print_result()
        else:
            result = self.word_list
        return result


def d_test():
    """
    类接口测试
    :return:
    """
    # s = '程序员(英文Programmer)是从事程序开发、维护的专业人员。' \
    #     '一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，' \
    #     '特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。'

    # s = '【今日题材】[AI决策]大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，' \
    #     '还是注册制的, 关注同花顺财经（ths58）， 获取更多机会。'

    s = '中兴通讯（000063）在经历七个一字跌停板后，于今天打开跌停板。债转股开盘大涨，天津普林（002134）、信达地产（600657）' \
        '、海德股份（000567）集体涨停，长航凤凰（000520）、浙江东方（600120）、陕国投A（000563）大涨，消息面上，' \
        '央行宣布定向降准0.5个百分点，将重点支持债转股。中兴通讯机构最低估值12.02元/股在复牌之前，' \
        '多家基金公司对中兴通讯估值大多调整至20.54元/股。连续7个跌停板后，中兴通讯A股股价早就已经跌穿这一价格。' \
        '据《中国经营报》记者不完全统计，6月20日～22日，多家基金公司再做出调整中兴通讯A股估值的公告，下调公司包括工银瑞信基金、' \
        '华泰柏瑞基金、东方基金、大摩华鑫基金、融通基金、大成基金等22家基金公司。值得注意的是，此次基金公司估值下调幅度并不一致，' \
        '调整估值在每股12.02～16.64元之间。其中，大摩华鑫基金、融通基金和安信基金给出的估值最高，为每股16.64元，而工银瑞信基金、' \
        '富国基金和泰达宏利基金给出的估值最低，为每股12.02元。关注同花顺财经（ths518），获取更多机会'

    # s = u"水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，" \
    #     u"根据刚刚完成了水资源管理制度的考核，有部分省接近了红线的指标，\n" \
    #     u"有部分省超过红线的指标。对一些超过红线的地方，\n陈明忠表示，对一些取用水项目进行区域的限批，" \
    #     u"严格地进行水资源论证和取水许可的批准。"

    data_process, dict_init, stop_words = DataPressing(), dicts.init(), load_stop_words()
    tk = tokenization.Tokenizer(data_process, dict_init, stop_words)
    s_list = tk.token(s)
    # 根据句子的长度，动态划分关键词的个数
    # top_k = int(len(s_list) * 0.1)
    # text_rank = TextRank(s_list, top_k=15, with_weight=True)

    text_rank = TextRank(top_k=15)
    res = text_rank.run(s_list)
    print("提取的%s个关键词: " % len(res))
    if text_rank.withWeight:
        print ",".join(item[0] for item in res)
        print ",".join(str(item[1]) for item in res)
    else:
        print ",".join(str(item) for item in res)


def parallel_test(text):
    text_rank = TextRank(top_k=15)
    return text_rank.run(text)


def multi_extract(s_lists):
    from multiprocessing import Pool, Queue, Process
    import multiprocessing as mp
    res_l = []
    pool = Pool(processes=int(mp.cpu_count()))
    for s_list in s_lists:
        res = pool.apply_async(parallel_test, (s_list,))
        res_l.append(res.get())
    pool.close()
    pool.join()

    return res_l


def multi_extract_test():
    """
    多进程测试
    :return:
    """
    import time
    from multiprocessing import Pool, Queue, Process
    import multiprocessing as mp

    s = '程序员(英文Programmer)是从事程序开发、维护的专业人员。' \
        '一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，' \
        '特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。'

    dataprocess = DataPressing()
    dict_init = dicts.init()
    stop_words = load_stop_words()
    # 分词
    tk = tokenization.Tokenizer(dataprocess, dict_init, stop_words)
    s_list = tk.token(s)
    t0 = time.time()
    for i in range(10000):
        parallel_test(s_list)
    print("串行处理花费时间{t}".format(t=time.time()-t0))

    pool = Pool(processes=int(mp.cpu_count()))
    res_l = []
    t1 = time.time()
    for i in range(10000):
        res = pool.apply_async(parallel_test, (s_list,))
        res_l.append(res)
    # pool.map(parallel_test, s_list)

    # for i in res_l:
    #     print i.get()
    pool.close()
    pool.join()
    print("并行处理花费时间{t}s".format(t=time.time()-t1))


if __name__ == '__main__':
    d_test()
    # multi_extract_test()
