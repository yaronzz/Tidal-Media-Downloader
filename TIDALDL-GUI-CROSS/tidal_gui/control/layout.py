#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  layout.py
@Date    :  2021/8/13
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtWidgets import QHBoxLayout


def createHBoxLayout(widgets):
    layout = QHBoxLayout()
    for item in widgets:
        layout.addWidget(item)
    return layout

