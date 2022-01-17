#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  pushButton.py
@Date    :  2021/05/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from tidal_gui.style import ButtonStyle


class PushButton(QPushButton):
    def __init__(self,
                 text: str = '',
                 style: ButtonStyle = ButtonStyle.Default,
                 width=0,
                 iconUrl=''):
        super(PushButton, self).__init__()
        self.setText(text)
        self.setObjectName(style.name + "PushButton")

        if width > 0:
            self.setFixedWidth(width)

        if iconUrl != '':
            self.setIcon(QIcon(iconUrl))
