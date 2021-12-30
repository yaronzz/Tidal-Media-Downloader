#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  aboutView.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel

from tidal_gui.control.label import Label
from tidal_gui.control.pushButton import PushButton
from tidal_gui.style import LabelStyle, ButtonStyle
from tidal_gui.theme import getResourcePath


class AboutView(QWidget):
    def __init__(self):
        super(AboutView, self).__init__()
        self.__initView__()

    def __initView__(self):
        grid = QGridLayout(self)
        grid.addWidget(self.__initLogo__(), 0, 0, Qt.AlignLeft)
        grid.addLayout(self.__initContent__(), 0, 1)

    def __initLogo__(self):
        path = getResourcePath() + "/svg/V.svg"
        self._logo = QLabel()
        self._logo.setPixmap(QPixmap(path))
        return self._logo

    def __initButton__(self):
        path = getResourcePath() + "/svg/"

        self._feedbackBtn = PushButton('Feedback', ButtonStyle.Default, iconUrl=path + 'github.svg')
        self._buymeacoffeeBtn = PushButton('Buymeacoffee', ButtonStyle.Info, iconUrl=path + 'buymeacoffee.svg')
        self._paypalBtn = PushButton('Paypal', ButtonStyle.Primary, iconUrl=path + 'paypal.svg')

        layout = QHBoxLayout()
        layout.addWidget(self._feedbackBtn)
        layout.addWidget(self._buymeacoffeeBtn)
        layout.addWidget(self._paypalBtn)
        return layout

    def __initContent__(self):
        self._titleLabel = Label('', LabelStyle.HugeTitle)
        self._authorLabel = Label('')
        self._versionLabel = Label('')
        self._lastVersionLabel = Label('')

        layout = QVBoxLayout()
        layout.addWidget(self._titleLabel)
        layout.addWidget(self._authorLabel)
        layout.addWidget(self._versionLabel)
        layout.addWidget(self._lastVersionLabel)
        layout.addLayout(self.__initButton__())
        return layout

    def setTitle(self, text: str):
        self._titleLabel.setText(text)

    def setAuthor(self, text: str):
        self._authorLabel.setText('MADE WITH ♥ BY ' + text)

    def setVersion(self, text: str):
        self._versionLabel.setText('VERSION ' + text)

    def setLastVersion(self, text: str):
        self._lastVersionLabel.setText('LAST-VERSION ' + text)
