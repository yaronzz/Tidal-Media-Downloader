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
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QGridLayout, QListWidgetItem

from tidal_gui.control.label import Label
from tidal_gui.control.line import Line
from tidal_gui.control.listWidget import ListWidget
from tidal_gui.style import LabelStyle, ListWidgetStyle
from tidal_gui.theme import getPackagePath


class TaskView(QWidget):
    def __init__(self):
        super(TaskView, self).__init__()
        self._listMap = {'Download': ListWidget(ListWidgetStyle.TaskContent),
                         'Complete': ListWidget(ListWidgetStyle.TaskContent),
                         'Error': ListWidget(ListWidgetStyle.TaskContent)}
        self._pageMap = {'Download': QWidget(),
                         'Complete': QWidget(),
                         'Error': QWidget()}
        self.__initView__()

    def __initView__(self):
        grid = QGridLayout(self)
        grid.addLayout(self.__initLefTab__(), 0, 0, Qt.AlignLeft)
        grid.addWidget(self.__createContent__('Download'), 0, 1, Qt.AlignTop)
        grid.addWidget(self.__createContent__('Complete'), 0, 1, Qt.AlignTop)
        grid.addWidget(self.__createContent__('Error'), 0, 1, Qt.AlignTop)

    def __initLefTab__(self):
        self._listTab = ListWidget(ListWidgetStyle.TaskTab)
        self._listTab.setIconSize(QSize(20, 20))

        iconPath = getPackagePath() + "/resource/svg/taskTab/"
        self._listTab.addIConTextItem(iconPath + 'download.svg', 'Download')
        self._listTab.addIConTextItem(iconPath + 'complete.svg', 'Complete')
        self._listTab.addIConTextItem(iconPath + 'Error.svg', 'Error')

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
        return self._pageMap[typeStr]

    def __tabItemChanged__(self, item: QListWidgetItem):
        for name in self._listMap:
            if name == item.text():
                self._pageMap[name].show()
            else:
                self._pageMap[name].hide()
    