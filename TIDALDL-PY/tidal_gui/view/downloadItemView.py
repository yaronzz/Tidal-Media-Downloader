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
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QVBoxLayout, QGridLayout, QProgressBar
from PyQt5.QtCore import Qt

from tidal_gui.control.label import Label
from tidal_gui.control.layout import createHBoxLayout, createVBoxLayout
from tidal_gui.control.pushButton import PushButton
from tidal_gui.style import LabelStyle, ButtonStyle


class DownloadItemView(QWidget):
    def __init__(self):
        super(DownloadItemView, self).__init__()
        self.__initView__()

    def __initView__(self):
        self._indexLabel = Label('1')
        self._titleLabel = Label('title', LabelStyle.Bold)
        self._ownLabel = Label('own')
        self._ownLabel.setMaximumWidth(200)
        self._actionLabel = Label('')
        self._actionLabel.setFixedWidth(80)
        self._errLabel = Label('')
        self._sizeLabel = Label('/')
        self._speedLabel = Label('')

        self._progress = QProgressBar()
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(3)
        self._progress.setFixedWidth(300)

        grid = QGridLayout(self)
        grid.addWidget(self._indexLabel, 0, 0, Qt.AlignLeft | Qt.AlignVCenter)
        grid.addWidget(self._titleLabel, 0, 1, Qt.AlignLeft | Qt.AlignVCenter)
        grid.addWidget(self._ownLabel, 0, 2, Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(self._progress, 0, 3, Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(self._actionLabel, 0, 4, Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(self._errLabel, 1, 1, Qt.AlignLeft | Qt.AlignVCenter)
        
        grid.setColumnStretch(1, 1)
        
        layout = QHBoxLayout()
        layout.setSpacing(30)
        layout.addWidget(self._sizeLabel)
        layout.addWidget(self._speedLabel)
        
        grid.addLayout(layout, 1, 3, Qt.AlignLeft | Qt.AlignVCenter)

    def setLabel(self, index, title, own):
        self._indexLabel.setText(str(index))
        self._titleLabel.setText(title)
        self._ownLabel.setText(own)

    def setErrmsg(self, msg):
        self._errLabel.setText(msg)

    def setAction(self, msg):
        self._actionLabel.setText(msg)

    def setProgress(self, value):
        self._progress.setValue(value)
        pass
    
    def setSize(self, curSize: str, totalSize: str):
        self._sizeLabel.setText(f'{curSize}/{totalSize}')
        
    def setSpeed(self, speed: str):
        self._speedLabel.setText(speed)
