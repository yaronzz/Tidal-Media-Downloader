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
from PyQt5.QtWidgets import QComboBox, QListView
from PyQt5.QtCore import Qt


class ComboBox(QComboBox):
    def __init__(self, items: list):
        super(ComboBox, self).__init__()
        self.setItems(items)
        self.setFixedWidth(200)
        self.setView(QListView())
        # remove shadow
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)

    def setItems(self, items):
        for item in items:
            self.addItem(str(item))