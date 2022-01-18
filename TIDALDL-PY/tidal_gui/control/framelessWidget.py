#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  framelessWidget.py
@Date    :  2021/05/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout

from tidal_gui.control.pushButton import PushButton
from tidal_gui.style import ButtonStyle


class FramelessWidget(QWidget):
    def __init__(self):
        super(FramelessWidget, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.BorderWidth = 5
        self.borderWidget = QWidget()
        self.borderWidget.setObjectName("widgetMain")
        self.borderWidget.setStyleSheet("QWidget#widgetMain{border: 1px solid #000000;};")

        self.contentGrid = QGridLayout()
        self.contentGrid.setContentsMargins(1, 1, 1, 1)

        self.windowBtnGrid = self.__createWindowsButtonLayout__()
        self.enableMove = True
        self.validMoveWidget = None
        self.clickPos = None

        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.addWidget(self.borderWidget, 0, 0)
        self.grid.addLayout(self.contentGrid, 0, 0)
        self.setLayout(self.grid)

    def __showMaxWindows__(self):
        if self.windowState() == Qt.WindowMaximized:
            self.showNormal()
        else:
            self.showMaximized()

    def __createWindowsButtonLayout__(self):
        self.closeBtn = PushButton('', ButtonStyle.CloseWindow)
        self.maxBtn = PushButton('', ButtonStyle.MaxWindow)
        self.minBtn = PushButton('', ButtonStyle.MinWindow)

        self.closeBtn.clicked.connect(self.close)
        self.minBtn.clicked.connect(self.showMinimized)
        self.maxBtn.clicked.connect(self.__showMaxWindows__)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(self.minBtn)
        layout.addWidget(self.maxBtn)
        layout.addWidget(self.closeBtn)
        return layout

    def __clickInValidMoveWidget__(self, x=-1, y=-1) -> bool:
        if self.validMoveWidget is None:
            return False
        if self.clickPos is None:
            return False
        
        if x == -1 and y == -1:
            x = self.clickPos.x()
            y = self.clickPos.y()

        pos = self.validMoveWidget.pos()
        if x < pos.x() or x > pos.x() + self.validMoveWidget.width():
            return False
        if y < pos.y() or y > pos.y() + self.validMoveWidget.height():
            return False
        return True

    def nativeEvent(self, eventType, message):
        retVal, result = super(FramelessWidget, self).nativeEvent(eventType, message)
        # if eventType == "windows_generic_MSG":
        #     msg = ctypes.wintypes.MSG.from_address(message.__int__())
        #     if msg.message != win32con.WM_NCHITTEST:
        #         return retVal, result

        #     # 获取鼠标移动经过时的坐标
        #     x = win32api.LOWORD(msg.lParam) - self.frameGeometry().x()
        #     y = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()

        #     w, h = self.width(), self.height()
        #     lx = x < self.BorderWidth
        #     rx = x > w - self.BorderWidth
        #     ty = y < self.BorderWidth
        #     by = y > h - self.BorderWidth
        #     if (lx and ty):# 左上角
        #         return True, win32con.HTTOPLEFT
        #     elif (rx and by):# 右下角
        #         return True, win32con.HTBOTTOMRIGHT
        #     elif (rx and ty):# 右上角
        #         return True, win32con.HTTOPRIGHT
        #     elif (lx and by):# 左下角
        #         return True, win32con.HTBOTTOMLEFT
        #     elif ty:# 上
        #         return True, win32con.HTTOP
        #     elif by:# 下
        #         return True, win32con.HTBOTTOM
        #     elif lx:# 左
        #         return True, win32con.HTLEFT
        #     elif rx:# 右
        #         return True, win32con.HTRIGHT
        return retVal, result

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self.clickPos = e.pos()

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self.clickPos = QPoint(-1, -1)

    def mouseMoveEvent(self, e: QMouseEvent):
        if not self.enableMove:
            return
        if Qt.LeftButton & e.buttons():
            if self.__clickInValidMoveWidget__() and self.clickPos:
                self.move(e.pos() + self.pos() - self.clickPos)

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        if self.maxBtn.isHidden():
            return
        if Qt.LeftButton & e.buttons():
            if self.__clickInValidMoveWidget__(e.x(), e.y()):
                self.__showMaxWindows__()

    def getGrid(self):
        return self.contentGrid

    def disableMove(self):
        self.enableMove = False

    def setValidMoveWidget(self, widget):
        self.validMoveWidget = widget

    def setWindowButton(self, showClose=True, showMin=True, showMax=True):
        if not showMax:
            self.maxBtn.hide()
        if not showMin:
            self.minBtn.hide()
        if not showClose:
            self.closeBtn.hide()
        self.grid.addLayout(self.windowBtnGrid, 0, 0, Qt.AlignTop | Qt.AlignRight)
