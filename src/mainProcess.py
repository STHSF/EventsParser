#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: mainProcess.py
@time: 2018/11/14 3:33 PM
"""
import os
import dataReader
import pandas as pd
import numpy as np
from gensim.models.word2vec import Word2Vec
from utills.Tokenization import load_stop_words
from utills.DataProcess import DataPressing
from utills import Tokenization, dicts, Vector
from utills import keywordsExtractor
from utills import news
from multiprocessing import Pool


class mainProcess(object):
    pass


if __name__ == '__main__':
    mp = mainProcess()
    # mp.data_save()
    # mp.word2vec_train()
    # model_w2v = mp.word2vec_load()
    # var = mp.word_vector(u'食品饮料', model_w2v)
    # print var
