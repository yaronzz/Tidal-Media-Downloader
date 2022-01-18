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
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout
from PyQt5.QtGui import QResizeEvent


class ScrollWidget(QScrollArea):
    def __init__(self):
        super(ScrollWidget, self).__init__()
        self._numWidget = 0
        self._layout = QVBoxLayout()
        self._layout.addStretch(1)

        self._mainW = QWidget()
        self._mainW.setLayout(self._layout)

        self.setWidget(self._mainW)
        self.setWidgetResizable(True)

    def addWidgetItem(self, widget: QWidget):
        self._layout.insertWidget(self._numWidget, widget)
        self._numWidget += 1
    
    def delWidgetItem(self, widget: QWidget):
        self._layout.removeWidget(widget)
        self._numWidget -= 1

    def resizeEvent(self, e: QResizeEvent):
        super().resizeEvent(e)
        width = e.size().width()
        if width > 0:
            self._mainW.setMaximumWidth(width)
        
