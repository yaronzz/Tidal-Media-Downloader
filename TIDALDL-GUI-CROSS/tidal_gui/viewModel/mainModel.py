#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  mainModel.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from tidal_gui.view.mainView import MainView
from tidal_gui.viewModel.aboutModel import AboutModel
from tidal_gui.viewModel.loginModel import LoginModel
from tidal_gui.viewModel.searchModel import SearchModel
from tidal_gui.viewModel.settingsModel import SettingsModel
from tidal_gui.viewModel.taskModel import TaskModel
from tidal_gui.viewModel.viewModel import ViewModel


class MainModel(ViewModel):
    def __init__(self):
        super(MainModel, self).__init__()
        self.loginModel = LoginModel()
        self.loginModel.SIGNAL_LOGIN_SUCCESS.connect(self.__loginSuccess__)

        self.searchModel = SearchModel()
        self.taskModel = TaskModel()
        self.settingsModel = SettingsModel()
        self.aboutModel = AboutModel()

        self.view = MainView()
        self.view.setSearchView(self.searchModel.view)
        self.view.setTaskView(self.taskModel.view)
        self.view.setSettingsView(self.settingsModel.view)
        self.view.setAboutView(self.aboutModel.view)

        self.view.showPage()

    def show(self):
        self.view.hide()
        self.loginModel.loginByConfig()
        self.loginModel.show()

    def __loginSuccess__(self):
        self.loginModel.hide()
        self.view.show()
