#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: news.py
@time: 2018/11/28 10:56 AM
"""


class news(object):
    def __init__(self, title, content, publish_time):
        self.title = title
        self.content = content
        self.publish_time = publish_time

    def title(self):
        return self.title()

    def content(self):
        return self.title()

    def publish_time(self):
        return self.publish_time()

    def news_detail(self):
        if self.title and self.content:
            print(self.title + self.content)

    def news_lists(self):
        pass
