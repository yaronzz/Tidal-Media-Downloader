#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  line.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtWidgets import QFrame


class Line(QFrame):
    def __init__(self, shape: str = 'V'):
        super(Line, self).__init__()
        self.setFrameShape(QFrame.VLine if shape == 'V' else QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

        self.setObjectName('VLineQFrame' if shape == 'V' else 'HLineQFrame')
