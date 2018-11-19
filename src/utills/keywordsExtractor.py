#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: keywordsExtractor.py
@time: 2018/11/19 10:19 AM
"""
import sys
import my_utils
import logging.handlers
import numpy as np
import Tokenization

LOG_FILE = '../log/keywordsExtractor.log'
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


class TextRank(object):
    def __init__(self, sentence, window, alpha, iternum):
        self.sentence = sentence
        self.window = window
        self.alpha = alpha
        self.edge_dict = {}  # 记录节点的边连接字典
        self.iternum = iternum  # 迭代次数

    def cutSentence(self):
        """
        # 对句子进行分词
        :return:
        """
        tk = Tokenization.Tokenizer()
        self.word_list = tk.token(self.sentence)
        # dicts.init()
        # jieba.load_userdict('user_dict.txt')
        # tag_filter = ['a', 'd', 'n', 'v']
        # seg_result = pseg.cut(self.sentence)
        # self.word_list = [s.word for s in seg_result if s.flag in tag_filter]
        # print(self.word_list)

    def createNodes(self):
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

    def createMatrix(self):
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
            sum = 0
            for i in range(self.matrix.shape[0]):
                sum += self.matrix[i][j]
            for i in range(self.matrix.shape[0]):
                self.matrix[i][j] /= sum

    def calPR(self):
        """
        # 根据textrank公式计算权重
        :return:
        """
        self.PR = np.ones([len(set(self.word_list)), 1])
        for i in range(self.iternum):
            self.PR = (1 - self.alpha) + self.alpha * np.dot(self.matrix, self.PR)

    def printResult(self):
        """
        # 输出词和相应的权重
        :return:
        """
        word_pr = {}
        for i in range(len(self.PR)):
            word_pr[self.index_dict[i]] = self.PR[i][0]
        res = sorted(word_pr.items(), key=lambda x: x[1], reverse=True)
        return res

    def run(self):
        if type(self.sentence) is not list:
            self.cutSentence()
        else:
            self.word_list = self.sentence
        self.createNodes()
        self.createMatrix()
        self.calPR()
        result = self.printResult()
        return result


if __name__ == '__main__':
    # s = '程序员(英文Programmer)是从事程序开发、维护的专业人员。一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。'
    s = '【今日题材】[AI决策]大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，还是注册制的, 关注同花顺财经（ths58）， 获取更多机会。'
    tk = Tokenization.Tokenizer()
    s_list = tk.token(s)
    tr = TextRank(s_list, 2, 0.85, 700)
    res = tr.run()
    for i in res:
        print "keyword\tweight"
        print(str(i[0]) + "\t" + str(i[1]))
        # print "keyword: %s, weight: %s" % (i[0], i[1])
