#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  settingsView.py
@Date    :  2021/05/11
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout

from tidal_gui.control.checkBox import CheckBox
from tidal_gui.control.comboBox import ComboBox
from tidal_gui.control.label import Label
from tidal_gui.control.line import Line
from tidal_gui.control.lineEdit import LineEdit
from tidal_gui.control.pushButton import PushButton
from tidal_gui.style import LabelStyle, ButtonStyle, ThemeStyle


class SettingsView(QWidget):
    def __init__(self):
        super(SettingsView, self).__init__()
        self.__initView__()

    def __initView__(self):
        grid = QVBoxLayout(self)
        grid.addLayout(self.__initHeader__())
        grid.addLayout(self.__initContent__())
        grid.addLayout(self.__initToolButton__())

    def __initHeader__(self):
        self._header = Label("SETTINGS", LabelStyle.PageTitle)
        layout = QVBoxLayout()
        layout.addWidget(self._header)
        layout.addWidget(Line('H'))
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 10)
        return layout

    def __initToolButton__(self) -> QHBoxLayout:
        self._logoutBtn = PushButton('Logout', ButtonStyle.Danger, 100)
        self._cancelBtn = PushButton('Cancel', ButtonStyle.Default, 100)
        self._confirmBtn = PushButton('OK', ButtonStyle.Primary, 100)

        layout = QHBoxLayout()
        layout.addWidget(self._logoutBtn)
        layout.addStretch(1)
        layout.addWidget(self._cancelBtn)
        layout.addWidget(self._confirmBtn)
        return layout

    def __addContent__(self, control, desc=''):
        rowIdx = self._contentLayout.rowCount()
        if desc != '':
            self._contentLayout.addWidget(Label(desc), rowIdx, 0, Qt.AlignRight)
        self._contentLayout.addWidget(control, rowIdx, 1)

    def __initContent__(self):
        self._contentLayout = QGridLayout()
        self._contentLayout.setSpacing(15)

        self._pathEdit = LineEdit()
        self._threadNumComboBox = ComboBox([1, 5, 10, 20])
        self._searchNumComboBox = ComboBox([10, 20, 30, 40, 50])
        self.__addContent__(self._pathEdit, 'Path:')
        self.__addContent__(self._threadNumComboBox, 'ThreadNum:')
        self.__addContent__(self._searchNumComboBox, 'SearchNum:')

        self._contentLayout.setRowStretch(self._contentLayout.rowCount(), 1)

        self._albumFolderFormatEdit = LineEdit()
        self._trackFileFormatEdit = LineEdit()
        self._videoFileFormatEdit = LineEdit()
        self.__addContent__(self._albumFolderFormatEdit, 'AlbumFolderFormat:')
        self.__addContent__(self._trackFileFormatEdit, 'TrackFileFormat:')
        self.__addContent__(self._videoFileFormatEdit, 'VideoFileFormat:')

        self._saveCoverCheck = CheckBox('Download album cover')
        self._skipExistCheck = CheckBox('Skip exist file when downloading')
        self._convertMp4ToM4a = CheckBox('Convert mp4 to m4a')
        self.__addContent__(self._saveCoverCheck)
        self.__addContent__(self._skipExistCheck)
        self.__addContent__(self._convertMp4ToM4a)

        self._contentLayout.setRowStretch(self._contentLayout.rowCount(), 1)

        self._themeComboBox = ComboBox(list(map(lambda x: x.name, ThemeStyle)))
        self._languageComboBox = ComboBox(['Default'])
        self.__addContent__(self._themeComboBox, 'Theme:')
        self.__addContent__(self._languageComboBox, 'Language:')

        self._contentLayout.setRowStretch(self._contentLayout.rowCount(), 10)
        return self._contentLayout

    def connectButton(self, name: str, func):
        if name == "Logout":
            self._logoutBtn.clicked.connect(func)
        elif name == "Cancel":
            self._cancelBtn.clicked.connect(func)
        elif name == "OK":
            self._confirmBtn.clicked.connect(func)
