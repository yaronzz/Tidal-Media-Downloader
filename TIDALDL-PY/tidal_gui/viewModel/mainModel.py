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
from tidal_gui.downloader import downloadImp
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
        self.searchModel = SearchModel()
        self.taskModel = TaskModel()
        self.settingsModel = SettingsModel(self)
        self.aboutModel = AboutModel()

        self.loginModel.SIGNAL_LOGIN_SUCCESS.connect(self.__loginSuccess__)
        self.searchModel.SIGNAL_ADD_TASKITEM.connect(self.taskModel.addTaskItem)

        self.view = MainView()
        self.view.setSearchView(self.searchModel.view)
        self.view.setTaskView(self.taskModel.view)
        self.view.setSettingsView(self.settingsModel.view)
        self.view.setAboutView(self.aboutModel.view)

        self.view.showPage()

        downloadImp.setTaskModel(self.taskModel)
        downloadImp.start()

    def uninit(self):
        self.taskModel.uninit()
        downloadImp.stop()

    def show(self, relogin: bool = False):
        self.view.hide()
        self.loginModel.login(bool(1 - relogin))
        self.loginModel.show()

    def __loginSuccess__(self):
        self.loginModel.hide()
        self.view.show()
