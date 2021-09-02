#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  settingsModel.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from tidal_gui.view.settingsView import SettingsView
from tidal_gui.viewModel.viewModel import ViewModel


class SettingsModel(ViewModel):
    def __init__(self):
        super(SettingsModel, self).__init__()
        self.view = SettingsView()
