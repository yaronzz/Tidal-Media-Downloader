#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  scrollWidget.py
@Date    :  2021/10/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget, QScrollArea, QVBoxLayout, QPushButton, QBoxLayout


class ScrollWidget(QScrollArea):
    def __init__(self):
        super(ScrollWidget, self).__init__()
        
        self._layout = QVBoxLayout()
        self._layout.addStretch(1)
        
        self._mainW = QWidget()
        self._mainW.setLayout(self._layout)
        
        self.setWidget(self._mainW)
        self.setWidgetResizable(True)

    def addWidgetItem(self, widget: QWidget):
        self._layout.insertWidget(0, widget)
