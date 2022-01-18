#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  downloadItemView.py
@Date    :  2021/10/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QProgressBar

from tidal_gui.control.label import Label
from tidal_gui.style import LabelStyle


class DownloadItemView(QWidget):
    def __init__(self):
        super(DownloadItemView, self).__init__()
        self.__initView__()
        self.setObjectName('DownloadItemView')
        self.setAttribute(Qt.WA_StyledBackground)

    def __initView__(self):
        self._indexLabel = Label('1')
        self._codecLabel = Label('', LabelStyle.Tag)
        self._titleLabel = Label('title', LabelStyle.Bold)
        self._ownLabel = Label('own', LabelStyle.Italic)
        self._ownLabel.setMaximumWidth(200)
        self._actionLabel = Label('', LabelStyle.Italic)
        self._actionLabel.setFixedWidth(80)
        
        self._errLabel = Label('')
        self._errLabel.setVisible(False)

        self._sizeLabel = Label('/')
        self._speedLabel = Label('')

        self._progress = QProgressBar()
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(3)
        self._progress.setFixedWidth(300)
        self._progress.setRange(0, 100)

        titleLayout = QHBoxLayout()
        titleLayout.setSpacing(3)
        titleLayout.setContentsMargins(0, 0, 0, 0)
        titleLayout.addWidget(self._indexLabel, Qt.AlignLeft)
        titleLayout.addWidget(self._titleLabel, Qt.AlignLeft)
        titleLayout.addStretch(50)
        titleLayout.addWidget(self._codecLabel, Qt.AlignRight)
        titleLayout.addWidget(self._ownLabel, Qt.AlignRight)
        
        speedLayout = QHBoxLayout()
        speedLayout.setSpacing(30)
        speedLayout.addWidget(self._sizeLabel)
        speedLayout.addWidget(self._speedLabel)

        grid = QGridLayout(self)
        grid.setContentsMargins(0,0,0,0)
        grid.setSpacing(2)
        grid.addLayout(titleLayout, 0, 0, Qt.AlignLeft | Qt.AlignVCenter)
        grid.addWidget(self._progress, 0, 1, Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(self._actionLabel, 0, 2, Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(self._errLabel, 1, 0, Qt.AlignLeft | Qt.AlignVCenter)
        grid.addLayout(speedLayout, 1, 1, Qt.AlignLeft | Qt.AlignVCenter)

    def setLabel(self, index, title, own):
        self._indexLabel.setText(str(index))
        self._titleLabel.setText(title)
        self._ownLabel.setText(own)

    def setErrmsg(self, msg):
        self._errLabel.setText(msg)
        self._errLabel.setVisible(len(msg) > 0)

    def setAction(self, msg):
        self._actionLabel.setText(msg)

    def setProgress(self, value):
        self._progress.setValue(value)
        pass

    def setSize(self, curSize: str, totalSize: str):
        self._sizeLabel.setText(f'{curSize} / {totalSize}')

    def setSpeed(self, speed: str):
        self._speedLabel.setText(speed)

    def setCodec(self, codec: str):
        self._codecLabel.setText(codec)
