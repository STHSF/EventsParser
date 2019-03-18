#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: tonghuashun.py
@time: 2018/10/30 11:13 AM
"""

import pyhanlp
import jpype
from jpype import *
# jvmPath = jpype.getDefaultJVMPath()
# print(jvmPath)
# # jpype.startJVM(jvmPath)
# jpype.java.lang.System.out.println("hello world!")
# java.lang.System.out.println("hello world")
# # jpype.shutdownJVM()


HanLP = JClass('com.hankcs.hanlp.HanLP')
#中文分词
print(HanLP.segment("你好，欢迎在Python中调用HanLP的API").toString())
testCases = [
    "商品和服务",
    "结婚的和尚未结婚的确实在干扰分词啊",
    "买水果然后来世博园最后去世博会",
    "中国的首都是北京",
    "欢迎新老师生前来就餐",
    "工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作",
    "随着页游兴起到现在的页游繁盛，依赖于存档进行逻辑判断的设计减少了，但这块也不能完全忽略掉。"]
for sentence in testCases: print(HanLP.segment(sentence))
# 命名实体识别与词性标注
NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
print(NLPTokenizer.segment('中国科学院计算技术研究所的宗成庆教授正在教授自然语言处理课程'))
# 关键词提取
document = "水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，" \
           "根据刚刚完成了水资源管理制度的考核，有部分省接近了红线的指标，" \
           "有部分省超过红线的指标。对一些超过红线的地方，陈明忠表示，对一些取用水项目进行区域的限批，" \
           "严格地进行水资源论证和取水许可的批准。"
print(HanLP.extractKeyword(document, 2))
# 自动摘要
print(HanLP.extractSummary(document, 2))
# 依存句法分析
print(HanLP.parseDependency("徐先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。"))
jpype.shutdownJVM()

