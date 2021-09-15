#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  taskItemView.py
@Date    :  2021/9/14
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QVBoxLayout

from tidal_gui.control.label import Label
from tidal_gui.control.layout import createHBoxLayout, createVBoxLayout
from tidal_gui.control.pushButton import PushButton


class TaskItemView(QWidget):
    def __init__(self):
        super(TaskItemView, self).__init__()
        self.__initView__()

    def __initView__(self):
        grid = QVBoxLayout(self)
        grid.addLayout(self.__initHead__())
        grid.addWidget(self.__initList__())

    def __initHead__(self):
        self._btnRetry = PushButton()
        self._btnCancel = PushButton()
        self._btnDelete = PushButton()
        self._btnOpen = PushButton()
        self._btnExpand = PushButton()
        btnLayout = createHBoxLayout([self._btnRetry, self._btnCancel,
                                      self._btnDelete, self._btnOpen,
                                      self._btnExpand])

        self._titleLabel = Label()
        self._descLabel = Label()
        self._errLabel = Label()
        self._errLabel.hide()
        labelLayout = createVBoxLayout([self._titleLabel, self._descLabel, self._errLabel])

        self._picLabel = Label()
        headLayout = QHBoxLayout()
        headLayout.addWidget(self._picLabel)
        headLayout.addLayout(labelLayout)
        headLayout.addStretch(1)
        headLayout.addLayout(btnLayout)

        return headLayout

    def __initList__(self):
        self._list = QTableWidget()
        return self._list

    def setLabel(self, title, desc):
        self._titleLabel.setText(title)
        self._descLabel.setText(desc)

    def setErrmsg(self, msg):
        self._errLabel.setText(msg)

    def setPic(self, data):
        pass

    def addList(self):
        pass
