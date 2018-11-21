#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: __init__.py.py
@time: 2018/10/30 10:45 AM
"""
# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
from multiprocessing import Pool, Queue, Process
import multiprocessing as mp
import time, random
import os
import codecs
import jieba.analyse

# jieba.analyse.set_stop_words("yy_stop_words.txt")


def extract_keyword(input_string):
    # print("Do task by process {proc}".format(proc=os.getpid()))
    tags = jieba.analyse.extract_tags(input_string, topK=100)
    # print("key words:{kw}".format(kw=" ".join(tags)))
    return tags


# def parallel_extract_keyword(input_string,out_file):
def parallel_extract_keyword(input_string):
    # print("Do task by process {proc}".format(proc=os.getpid()))
    tags = jieba.analyse.extract_tags(input_string, topK=100)
    # time.sleep(random.random())
    # print("key words:{kw}".format(kw=" ".join(tags)))
    # o_f = open(out_file,'w')
    # o_f.write(" ".join(tags)+"\n")
    return tags


if __name__ == "__main__":

    lines = '程序员(英文Programmer)是从事程序开发、维护的专业人员。' \
        '一般将程序员分为程序设计人员和程序编码人员，但两者的界限并不非常清楚，' \
        '特别是在中国。软件从业人员分为初级程序员、高级程序员、系统分析员和项目经理四大类。'
    # out_put = data_file.split('.')[0] + "_tags.txt"
    t0 = time.time()
    for line in lines:
        parallel_extract_keyword(line)
        # parallel_extract_keyword(line,out_put)
        # extract_keyword(line)
    print("串行处理花费时间{t}".format(t=time.time() - t0))

    pool = Pool(processes=int(mp.cpu_count() * 0.7))
    t1 = time.time()
    # for line in lines:
    res = pool.apply_async(parallel_extract_keyword, (lines,))
    # 保存处理的结果，可以方便输出到文件
    # res = pool.map(parallel_extract_keyword, lines)
    print("Print keywords:")
    for tag in res.get():
        print tag
        # print(",".join(tag))
    pool.close()
    pool.join()
    print("并行处理花费时间{t}s".format(t=time.time() - t1))