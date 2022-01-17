#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  loginModel.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import _thread
import webbrowser

from PyQt5.QtCore import pyqtSignal
from tidal_dl.util import API, loginByConfig, loginByWeb

from tidal_gui.view.loginView import LoginView
from tidal_gui.viewModel.viewModel import ViewModel


class LoginModel(ViewModel):
    SIGNAL_LOGIN_SUCCESS = pyqtSignal()

    def __init__(self):
        super(LoginModel, self).__init__()
        self.view = LoginView()
        self.view.connectConfirmButton(self.__openWeb__)
        self.SIGNAL_REFRESH_VIEW.connect(self.__refresh__)

    def __refresh__(self, stype: str, text: str):
        if stype == "userCode":
            self.view.setDeviceCode(text)
            self.view.enableConfirmButton(True)
            self.view.setMsg(' ')
            self.view.showEnterView()
        elif stype == "showMsg":
            self.view.hideEnterView()
            self.view.setMsg(text)

    def login(self, useConfig=True):
        self.SIGNAL_REFRESH_VIEW.emit('showMsg', "LOGIN...")

        def __thread_login__(model: LoginModel, useConfig: bool):
            if useConfig and loginByConfig():
                model.SIGNAL_LOGIN_SUCCESS.emit()
                return
            model.getDeviceCode()

        _thread.start_new_thread(__thread_login__, (self, useConfig))

    def getDeviceCode(self):
        self.SIGNAL_REFRESH_VIEW.emit('showMsg', "GET DEVICE-CODE...")

        def __thread_getCode__(model: LoginModel):
            msg, check = API.getDeviceCode()
            if check:
                model.SIGNAL_REFRESH_VIEW.emit('userCode', API.key.userCode)
            else:
                model.SIGNAL_REFRESH_VIEW.emit('showMsg', msg)

        _thread.start_new_thread(__thread_getCode__, (self,))

    def __openWeb__(self):
        self.view.enableConfirmButton(False)
        webbrowser.open('http://link.tidal.com/' + API.key.userCode, new=0, autoraise=True)

        def __thread_waitLogin__(model: LoginModel):
            if loginByWeb():
                model.SIGNAL_LOGIN_SUCCESS.emit()
            else:
                model.getDeviceCode()

        _thread.start_new_thread(__thread_waitLogin__, (self,))
