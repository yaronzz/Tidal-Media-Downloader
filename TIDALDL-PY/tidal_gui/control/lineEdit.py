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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QAction


class LineEdit(QLineEdit):
    def __init__(self, placeholderText: str = "", iconUrl: str = ''):
        super(LineEdit, self).__init__()
        self.setPlaceholderText(placeholderText)

        if iconUrl != '':
            action = QAction(self)
            action.setIcon(QIcon(iconUrl))
            self.addAction(action, QLineEdit.LeadingPosition)
