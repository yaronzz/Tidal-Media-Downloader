#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  checkBox.py
@Date    :  2021/05/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""

from PyQt5.QtWidgets import QCheckBox


class CheckBox(QCheckBox):
    def __init__(self, text: str = "", checked: bool = False):
        super(CheckBox, self).__init__()
        self.setChecked(checked)
        self.setText(text)
