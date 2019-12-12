#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: li
@file: __init__.py.py
@time: 2019-03-05 10:33
"""
import argparse
import datetime
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    date = str(datetime.date.today().strftime("%Y-%m-%d"))
    parser.add_argument('--start_date', type=str, default=date)
    parser.add_argument('--end_date', type=int, default=0)
    parser.add_argument('--count', type=int, default=10)
    parser.add_argument('--rebuild', type=bool, default=False)
    parser.add_argument('--schedule', type=bool, default=False)

    args = parser.parse_args()
    print(args.start_date)