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
    def __init__(self, parent):
        super(SettingsModel, self).__init__()
        self._parent = parent
        self.view = SettingsView()
        self.view.connectButton('Logout', self.__logout__)
        self.view.connectButton('Cancel', self.__cancel__)
        self.view.connectButton('OK', self.__ok__)
    
    def __logout__(self):
        self._parent.show(True)
    
    def __cancel__(self):
        pass

    def __ok__(self):
        pass
