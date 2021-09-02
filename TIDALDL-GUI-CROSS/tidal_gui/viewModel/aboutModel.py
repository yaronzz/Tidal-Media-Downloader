#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  aboutModel.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from tidal_gui.view.aboutView import AboutView
from tidal_gui.viewModel.viewModel import ViewModel


class AboutModel(ViewModel):
    def __init__(self):
        super(AboutModel, self).__init__()
        self.view = AboutView()
        self.view.setTitle('TIDAL-GUI')
        self.view.setAuthor('Yaronzz')
        self.view.setVersion('1.0.0.1')
        self.view.setLastVersion('1.0.0.1')
