#!/usr/bin/env python
# encoding: utf-8
'''
@license: (C) Copyright 2013-2020, Node Supply Chain Manager Corporation Limited.
@time: 2023/5/11 14:51
@file: data_helper.py
@author: zsc
@Software: PyCharm
@desc:
'''
import pandas as pd

def load_data(filename):
    """
    加载数据
    单条格式：(文本, 标签id)
    :param filename:
    :return:
    """
    df = pd.read_csv(filename, header=0)
    return df[['text', 'label']].values


