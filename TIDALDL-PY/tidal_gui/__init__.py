#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  __init__.py
@Date    :  2021/05/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import sys

from PyQt5.QtWidgets import QApplication

from tidal_gui import theme
from tidal_gui.viewModel.mainModel import MainModel


def main():
    qss = theme.getThemeQssContent()
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)

    mainView = MainModel()
    mainView.show()

    app.exec_()
    mainView.uninit()

    sys.exit()


if __name__ == '__main__':
    main()
