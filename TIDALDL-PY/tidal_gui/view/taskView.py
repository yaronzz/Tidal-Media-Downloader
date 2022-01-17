#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  taskView.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from enum import Enum

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QGridLayout, QListWidgetItem

from tidal_gui.control.label import Label
from tidal_gui.control.line import Line
from tidal_gui.control.listWidget import ListWidget
from tidal_gui.control.scrollWidget import ScrollWidget
from tidal_gui.style import LabelStyle, ListWidgetStyle
from tidal_gui.theme import getResourcePath


class TaskListType(Enum):
    Download = 0,
    Complete = 1,
    Error = 2,


class TaskView(QWidget):
    def __init__(self):
        super(TaskView, self).__init__()
        self._listMap = {}
        self._pageMap = {}

        for item in map(lambda typeItem: typeItem.name, TaskListType):
            self._listMap[item] = ScrollWidget()
            self._pageMap[item] = QWidget()

        self.__initView__()
        self._listTab.setCurrentRow(0)
        self._pageMap[TaskListType.Download.name].show()

    def __initView__(self):
        grid = QGridLayout(self)
        grid.addLayout(self.__initLefTab__(), 0, 0, Qt.AlignLeft)
        for item in map(lambda typeItem: typeItem.name, TaskListType):
            grid.addWidget(self.__createContent__(item), 0, 1)

    def __initLefTab__(self):
        self._listTab = ListWidget(ListWidgetStyle.TaskTab)
        self._listTab.setIconSize(QSize(20, 20))

        iconPath = getResourcePath() + "/svg/taskTab/"
        self._listTab.addIConTextItem(iconPath + 'download.svg', TaskListType.Download.name)
        self._listTab.addIConTextItem(iconPath + 'complete.svg', TaskListType.Complete.name)
        self._listTab.addIConTextItem(iconPath + 'error.svg', TaskListType.Error.name)

        self._listTab.itemClicked.connect(self.__tabItemChanged__)

        layout = QGridLayout()
        layout.addWidget(Label("TASK LIST", LabelStyle.PageTitle), 0, 0, Qt.AlignLeft)
        layout.addWidget(self._listTab, 1, 0, Qt.AlignLeft)
        layout.addWidget(Line('V'), 0, 1, 2, 1, Qt.AlignLeft)
        return layout

    def __createContent__(self, typeStr: str):
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 10, 10)
        layout.setSpacing(10)
        layout.addWidget(Label(typeStr, LabelStyle.PageSubTitle), 0, 0, Qt.AlignTop)
        layout.addWidget(Line('H'), 1, 0, Qt.AlignTop)
        layout.addWidget(self._listMap[typeStr], 2, 0)

        self._pageMap[typeStr].setLayout(layout)
        self._pageMap[typeStr].hide()
        return self._pageMap[typeStr]

    def __tabItemChanged__(self, item: QListWidgetItem):
        for name in self._listMap:
            if name == item.text():
                self._pageMap[name].show()
            else:
                self._pageMap[name].hide()

    def addItemView(self, stype: TaskListType, view):
        self._listMap[stype.name].addWidgetItem(view)
