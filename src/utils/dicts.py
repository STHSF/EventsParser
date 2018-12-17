#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: li
@file: dicts.py
@time: 2018/11/5 2:31 PM
jieba 字典初始化模块
功能：添加用户自定义词典，结巴添加新词
如果有新登陆词，可以在corpus中的新增中添加
"""

import jieba
import codecs
from src.configure import conf
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

deg_dict = {}     # 程度副词
senti_dict = {}   # 情感词
eng_dict = {}     # 英语或拼音词
fou_dict = []     # 否定词
but_dict = []     # 转折词
lim_dict = []     # 限定词
new_dict = []     # 新词
zhi_dict = []     # 知网
stock_dict = []   # 股票词
stock_code_dict = []  # 股票代码
jg_dict = []  # 机构名


def init():
    # dic_path = '/Users/li/PycharmProjects/huihongcaihui/src/corpus'
    dic_path = conf.dic_path

    # 读取词典
    d_path = dic_path + "/程度副词_datatang.txt"
    s_path = dic_path + "/senti.txt"
    f_path = dic_path + "/fou.txt"
    b_path = dic_path + "/but.txt"
    e_path = dic_path + "/eng.txt"
    l_path = dic_path + "/limit.dict"
    a_path = dic_path + "/dic.txt"
    ns_path = dic_path + "/新增_stock"
    n_path = dic_path + "/新增"
    st_path = dic_path + "/stock_words.txt"
    zhi_ne_path = dic_path + "/知网/zhi_neg.txt"
    zhi_po_path = dic_path + "/知网/zhi_pos.txt"
    jg_path = dic_path + "/机构"

    # 添加基金公司实体名字，比如("工银瑞信基金"， "华泰柏瑞基金"， "东方基金")

    # 结巴新词
    word_add = set()

    for d in open(d_path):
        # temp = d.decode("utf-8").split(" ")
        temp = d.split(" ")
        word_arr = temp[1].strip("\n").rstrip(" ").split("、")
        for w in word_arr:
            deg_dict[w] = float(temp[0])
            word_add.add(temp[0])

    for s in open(s_path):
        temp = s.decode("utf-8").split(" ")
        senti_dict[temp[0]] = float(temp[1])
        word_add.add(temp[0])

    for e in open(e_path):
        temp = e.split(" ")
        eng_dict[temp[0]] = float(temp[1])
        word_add.add(temp[0])

    for f in open(f_path):
        f = f.decode("utf-8-sig")
        fou_dict.append(f.strip("\n"))
        word_add.add(f.strip("\n"))

    for b in open(b_path):
        but_dict.append(b.strip("\n"))
        word_add.add(b.strip("\n"))

    for l in open(l_path):
        lim_dict.append(l.strip("\n"))
        word_add.add(l.strip("\n"))

    for a in open(a_path):
        new_dict.append(a.strip("\n"))
        word_add.add(a.strip("\n"))

    for st in open(st_path):
        st = st.decode("utf8")
        code1, st_code = st.split("\t")
        code, stock = st_code.split(",")
        stock_code_dict.append(code.strip("\n"))
        stock_dict.append(stock.strip("\n"))
        word_add.add(code.strip("\n"))
        word_add.add(stock.strip("\n"))

    for z1 in open(zhi_ne_path):
        z1 = z1.decode("utf8")
        new_dict.append(z1.strip("\n"))
        word_add.add(z1.strip("\n"))

    for z2 in open(zhi_po_path):
        z2 = z2.decode("utf8")
        z2_data = z2.strip("\n")
        new_dict.append(z2_data)
        word_add.add(z2_data)

    for jg in open(jg_path):
        jg = jg.decode("utf8")
        jg_data = jg.split("\t")[0].strip("\n")
        new_dict.append(jg_data)
        word_add.add(jg_data)

    '''
    # 将stock_words.txt中的股票词转换成jieba用户自定义词典的格式，然后添加到jieba的userdict中
    for st in open(st_path):
        code1, st_code = st.split("\t")
        code, stock = st_code.split(",")
        stock_dict.append(code + ' ' + '5' + ' ' + 'n')
        stock_dict.append(stock.strip('\n').decode('utf-8') + ' ' + '5' + ' ' + 'n')
    f = codecs.open(n_path, 'w', 'utf-8')
    for i in stock_dict:
        f.write(i + '\n')  # \n为换行符
    f.close()
    '''
    # 添加用户自定义字典
    jieba.load_userdict(ns_path)
    jieba.load_userdict(n_path)
    jieba.load_userdict(jg_path)

    # 添加新词
    for w in word_add:
        jieba.add_word(w)

    # 结巴添加新词
    jieba.add_word("淡定")
    # jieba.add_word("加多宝")
    # jieba.add_word("红罐")
    jieba.add_word("非公开")
    jieba.add_word("不成人形")
    jieba.add_word("中美贸易战")
    print("[Info] jieba总共添加了{}个自定义词汇。".format(len(word_add)))


if __name__ == '__main__':
    init()