#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: test.py
@time: 2018/11/12 2:19 PM
"""
import sys
sys.path.append("..")
from gensim import corpora, models, similarities
from Tokenization import Tokenizer
from configure import Configure
from DataProcess import DataPressing


conf = Configure()


raw_documents = [
    u'0无偿居间介绍买卖毒品的行为应如何定性',
    u'1吸毒男动态持有大量毒品的行为该如何认定',
    u'2如何区分是非法种植毒品原植物罪还是非法制造毒品罪',
    u'3为毒贩贩卖毒品提供帮助构成贩卖毒品罪',
    u'4将自己吸食的毒品原价转让给朋友吸食的行为该如何认定',
    u'5为获报酬帮人购买毒品的行为该如何认定',
    u'6毒贩出狱后再次够买毒品途中被抓的行为认定',
    u'7虚夸毒品功效劝人吸食毒品的行为该如何认定',
    u'8妻子下落不明丈夫又与他人登记结婚是否为无效婚姻',
    u'9一方未签字办理的结婚登记是否有效',
    u'10夫妻双方1990年按农村习俗举办婚礼没有结婚证 一方可否起诉离婚',
    u'11结婚前对方父母出资购买的住房写我们二人的名字有效吗',
    u'12身份证被别人冒用无法登记结婚怎么办？',
    u'13同居后又与他人登记结婚是否构成重婚罪',
    u'14未办登记只举办结婚仪式可起诉离婚吗',
    u'15同居多年未办理结婚登记，是否可以向法院起诉要求离婚'
]


# def tokenization(filename):
#     """
#     对语料进行分词，分词之后先按照词性过滤出一些停用词，然后在通过停用词表过滤掉一些停用词。
#     :param filename:
#     :return:
#     """
#     dicts.init()  # 初始化人工词典
#     result = []
#     with open(filename, 'r') as f:
#         text = f.read()
#         words = pseg.cut(text)
#     for word, flag in words:
#         if flag not in stop_flag and word not in stopwords:
#             result.append(word)
#     return result


# 语料库准备，导入所有的语料，并且进行分词，去停用词
# filenames = ['/Users/yiiyuanliu/Desktop/nlp/demo/articles/13 件小事帮您稳血压.txt',
#              '/Users/yiiyuanliu/Desktop/nlp/demo/articles/高血压患者宜喝低脂奶.txt',
#              '/Users/yiiyuanliu/Desktop/nlp/demo/articles/ios.txt']


# corpus = []
# t = Tokenizer()
#
# for each in raw_documents:
#     corpus.append(t.token(each))
# print len(corpus)
#
#
# for item in corpus[0]:
#     print item
#
#
# def DictionaryBuild(corpus):
#     # 建立词袋模型。
#     dictionary = corpora.Dictionary(corpus)
#     return dictionary
#
#
# dictionary = DictionaryBuild(corpus)
# print dictionary
#
#
# def docVectors(dictionary):
#     doc_vectors = [dictionary.doc2bow(text) for text in corpus]
#     print len(doc_vectors)
#     print doc_vectors
#
# docVectors(dictionary)


# query = tokenization('/Users/yiiyuanliu/Desktop/nlp/demo/articles/关于降压药的五个问题.txt')
# query_bow = dictionary.doc2bow(query)
# print query_bow
#
#
# # 文本相似度计算
# # 基于积累的事件，首先计算所有事件的词向量或者tf-idf值，然后将新晋事件与最近的事件进行相似度计算，计算
# lsi = models.LsiModel(tfidf_vectors, id2word=dictionary, num_topics=2)


if __name__ == '__main__':
    import dicts
    stock_dict = dicts.stock_dict
    t = Tokenizer()
    data_processing = DataPressing()
    print(["大智慧".decode("utf8")])
    a = ["大智慧".decode("utf8")]
    print(len(a[0]))
    # print(["【今日题材】".decode("utf8")])

    # file = open('file_name.txt', 'w')
    # file.write(str(raw_documents))
    # file.close()

    # 剔除杂质词
    print(data_processing.no_remove("【今日题材】[AI决策]大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，还是注册制的"))

    # 判断content中是否存在某些特殊词
    print(data_processing.useless_remove("[AI决策]大智慧的股票真烂，中美贸易战打得好，中美贸易摩擦擦出爱情火花！科创板也上市了，还是注册制的"))

    # 筛选新闻，筛选出股市收报
    # str = '午后，分散染料概念股走强。截至发稿，浙江龙盛(600352)[AI决策](浙江龙盛(600352)[AI决策]-CN)涨6.74%报13.15元，闰土股份(002440)[AI决策](闰土股份(002440)[AI决策]-CN)涨5.84%报19.94元，安诺其(300067)[AI决策](安诺其(300067)[AI决策]-CN)涨5.46%报6.38元，吉华集团(603980)[AI决策](吉华集团(603980)[AI决策]-CN)涨3.41%报22.42元，航民股份(600987)[AI决策](航民股份(600987)[AI决策]-CN)、江苏吴中(600200)[AI决策](江苏吴中(600200)[AI决策]-CN)等个股跟随上涨近2%。据分散染料龙头企业介绍，由于环保形势的持续严峻，企业开工受到限制，染料供应量较少，库存偏低。染料贸易商和印染企业前期采购的分散染料，经过四季度的消耗库存已经很低，近期需要补仓，刚需力度增强。推荐阅读：浙江龙盛最新消息'
    # a = t.token(str)
    # aa = data_processing.useless_filter(a, stock_dict)
    # print aa






