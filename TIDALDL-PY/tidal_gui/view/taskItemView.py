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
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QVBoxLayout, QListView, QGridLayout
from PyQt5.QtCore import Qt, QPoint

from tidal_gui.control.label import Label
from tidal_gui.control.layout import createHBoxLayout, createVBoxLayout
from tidal_gui.control.pushButton import PushButton
from tidal_gui.control.listWidget import ListWidget
from tidal_gui.style import LabelStyle, ButtonStyle, ListWidgetStyle


class TaskItemView(QWidget):
    def __init__(self):
        super().__init__()
        self.__initView__()
        self.setObjectName('TaskItemView')
        self.setAttribute(Qt.WA_StyledBackground)
                
    def __initView__(self):
        layout = QVBoxLayout()
        layout.addLayout(self.__initHead__(), Qt.AlignTop)
        layout.addWidget(self.__initList__(), Qt.AlignTop)
        
        self.setLayout(layout)

    def __initHead__(self):
        self._btnRetry = PushButton('', ButtonStyle.TaskRetry)
        self._btnCancel = PushButton('', ButtonStyle.TaskCancel)
        self._btnDelete = PushButton('', ButtonStyle.TaskDelete)
        self._btnOpen = PushButton('', ButtonStyle.TaskOpen)
        self._btnExpand = PushButton('', ButtonStyle.TaskExpand)
        self._btnExpand.clicked.connect(self.__expandClick__)
        btnLayout = createHBoxLayout([self._btnRetry, self._btnCancel,
                                      self._btnDelete, self._btnOpen,
                                      self._btnExpand])

        self._titleLabel = Label('', LabelStyle.PageTitle)
        self._descLabel = Label()
        self._errLabel = Label()
        self._errLabel.hide()
        labelLayout = createVBoxLayout([self._titleLabel, self._descLabel, self._errLabel])

        self._picLabel = Label('', LabelStyle.Icon)
        self._picLabel.setMinimumHeight(64)
        headLayout = QHBoxLayout()
        headLayout.addWidget(self._picLabel)
        headLayout.addLayout(labelLayout)
        headLayout.addStretch(1)
        headLayout.addLayout(btnLayout)

        return headLayout

    def __initList__(self):
        self._list = ListWidget(ListWidgetStyle.DownloadItems)
        self._list.setResizeMode(QListView.Adjust)
        return self._list

    def setLabel(self, title, desc):
        self._titleLabel.setText(title)
        self._descLabel.setText(desc)

    def setErrmsg(self, msg):
        self._errLabel.setText(msg)

    def setPic(self, data):
        pic = QPixmap()
        pic.loadFromData(data)
        self._picLabel.setPixmap(pic.scaled(64, 64))

    def addListItem(self, view):
        self._list.addWidgetItem(view)

    def __expandClick__(self):
        if self._list.isHidden():
            self._list.show()
        else:
            self._list.hide()

    def connectButton(self, name: str, func):
        if name == 'retry':
            self._btnRetry.clicked.connect(func)
        elif name == 'cancel':
            self._btnCancel.clicked.connect(func)
        elif name == 'delete':
            self._btnDelete.clicked.connect(func)
        elif name == 'open':
            self._btnOpen.clicked.connect(func)

