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
import time
import webbrowser

from PyQt5.QtCore import QTimer, pyqtSignal, QObject

from tidal_gui.tidalImp import tidalImp
from tidal_gui.view.loginView import LoginView
from tidal_gui.viewModel.viewModel import ViewModel


class LoginModel(ViewModel):
    SIGNAL_LOGIN_SUCCESS = pyqtSignal()

    def __init__(self):
        super(LoginModel, self).__init__()
        self.view = LoginView()
        self.view.connectConfirmButton(self.__openWebAndWait__)

    def loginByConfig(self):
        self.view.hideEnterView()
        self.view.setMsg("LOGIN...")

        def __thread_login__(model: LoginModel):
            if tidalImp.loginByConfig():
                model.SIGNAL_LOGIN_SUCCESS.emit()
                return
            model.getDeviceCode()

        _thread.start_new_thread(__thread_login__, (self,))

    def getDeviceCode(self):
        self.view.hideEnterView()
        self.view.setMsg("GET DEVICE-CODE...")

        def __thread_getCode__(model: LoginModel):
            msg, check = tidalImp.getDeviceCode()
            if check:
                model.view.enableConfirmButton(True)
                model.view.setDeviceCode(tidalImp.key.userCode)
                model.view.setMsg(' ')
                model.view.showEnterView()
            else:
                model.view.setMsg(msg)

        _thread.start_new_thread(__thread_getCode__, (self,))

    def __openWebAndWait__(self):
        self.view.enableConfirmButton(False)
        webbrowser.open('link.tidal.com', new=0, autoraise=True)

        def __thread_waitLogin__(model: LoginModel):
            if tidalImp.loginByWeb():
                model.SIGNAL_LOGIN_SUCCESS.emit()
            else:
                model.getDeviceCode()

        _thread.start_new_thread(__thread_waitLogin__, (self,))
