#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  label.py
@Date    :  2021/05/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtWidgets import QLabel

from tidal_gui.style import LabelStyle


class Label(QLabel):
    def __init__(self, text: str = "", style: LabelStyle = LabelStyle.Default):
        super(Label, self).__init__()
        self.setText(text)
        self.setObjectName(style.name + "Label")
