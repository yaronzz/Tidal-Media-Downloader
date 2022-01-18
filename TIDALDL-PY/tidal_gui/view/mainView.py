#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  main.py
@Date    :  2021/05/11
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from enum import IntEnum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QGridLayout

from tidal_gui.control.framelessWidget import FramelessWidget
from tidal_gui.control.pushButton import PushButton
from tidal_gui.style import ButtonStyle


class PageType(IntEnum):
    Search = 0,
    Task = 1,
    Settings = 2,
    About = 3,
    Max = 4,


class MainView(FramelessWidget):
    viewWidth = 1200
    viewHeight = 700

    def __init__(self):
        super(MainView, self).__init__()
        self.setMinimumHeight(self.viewHeight)
        self.setMinimumWidth(self.viewWidth)
        self.__initPages__()
        self.__initView__()
        self.setWindowButton(True, True, True)

    def __initPages__(self):
        self._pages = []
        for index in range(0, PageType.Max):
            self._pages.append(None)

    def __initView__(self):
        leftTab = self.__initLeftTab__()
        content = self.__initContent__()
        moveWgt = self.__initMoveHead__()

        grid = self.getGrid()
        grid.addWidget(leftTab, 0, 0, 2, 1, Qt.AlignLeft)
        grid.addWidget(moveWgt, 0, 1, Qt.AlignTop)
        grid.addLayout(content, 1, 1)

        self.setValidMoveWidget(moveWgt)

    def __initLeftTab__(self):
        self._icon = PushButton("", ButtonStyle.SoftwareIcon)
        self._searchBtn = PushButton("", ButtonStyle.SearchIcon)
        self._taskBtn = PushButton("", ButtonStyle.TaskIcon)
        self._settingsBtn = PushButton("", ButtonStyle.SettingsIcon)
        self._aboutBtn = PushButton("", ButtonStyle.AboutIcon)

        self._searchBtn.clicked.connect(lambda: self.showPage(PageType.Search))
        self._taskBtn.clicked.connect(lambda: self.showPage(PageType.Task))
        self._settingsBtn.clicked.connect(lambda: self.showPage(PageType.Settings))
        self._aboutBtn.clicked.connect(lambda: self.showPage(PageType.About))

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 45, 15, 20)
        layout.addWidget(self._icon)
        layout.addWidget(self._searchBtn)
        layout.addWidget(self._taskBtn)
        layout.addStretch(1)
        # layout.addWidget(self._settingsBtn)
        # layout.addWidget(self._aboutBtn)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setObjectName("MainViewLeftWidget")
        return widget

    def __initMoveHead__(self) -> QWidget:
        self._moveWidget = QWidget()
        self._moveWidget.setFixedHeight(30)
        self._moveWidget.setObjectName("BaseWidget")
        return self._moveWidget

    def __initContent__(self) -> QGridLayout:
        self._searchView = None
        self._settingsView = None
        self._aboutView = None
        self._taskView = None
        self._contentLayout = QGridLayout()
        self._contentLayout.setContentsMargins(10, 0, 10, 10)
        return self._contentLayout

    def showPage(self, pageType: PageType = PageType.Search):
        for index in range(0, PageType.Max):
            if index == pageType:
                self._pages[index].show()
            else:
                self._pages[index].hide()

    def __setContentPage__(self, view, pageType: PageType):
        self._pages[pageType] = view
        self._pages[pageType].hide()
        self._contentLayout.addWidget(view, 0, 0)

    def setSearchView(self, view):
        self.__setContentPage__(view, PageType.Search)

    def setTaskView(self, view):
        self.__setContentPage__(view, PageType.Task)

    def setSettingsView(self, view):
        self.__setContentPage__(view, PageType.Settings)

    def setAboutView(self, view: QWidget):
        self._pages[PageType.About] = view
        self._pages[PageType.About].hide()
