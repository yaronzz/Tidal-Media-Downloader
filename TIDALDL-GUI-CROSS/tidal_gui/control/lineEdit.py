#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  lineEdit.py
@Date    :  2021/05/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtWidgets import QLineEdit


class LineEdit(QLineEdit):
    def __init__(self, placeholderText: str = ""):
        super(LineEdit, self).__init__()
        self.setPlaceholderText(placeholderText)
