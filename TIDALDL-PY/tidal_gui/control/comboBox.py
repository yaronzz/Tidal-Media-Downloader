#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  comboBox.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QListView


class ComboBox(QComboBox):
    def __init__(self, items: list, width: int = 200):
        super(ComboBox, self).__init__()
        self.setItems(items)
        self.setFixedWidth(width)
        self.setView(QListView())
        # remove shadow
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)

    def setItems(self, items):
        for item in items:
            self.addItem(str(item))
