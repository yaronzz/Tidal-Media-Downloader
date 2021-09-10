#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  searchView.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import tidal_dl.model
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget

from tidal_gui.control.comboBox import ComboBox
from tidal_gui.control.label import Label
from tidal_gui.control.layout import createHBoxLayout
from tidal_gui.control.lineEdit import LineEdit
from tidal_gui.control.pushButton import PushButton
from tidal_gui.control.tableWidget import TableWidget
from tidal_gui.style import ButtonStyle
from tidal_gui.theme import getPackagePath


class SearchView(QWidget):
    def __init__(self):
        super(SearchView, self).__init__()
        self._rowCount = 20
        self.__initView__()

    def __initView__(self):
        grid = QVBoxLayout(self)
        grid.addLayout(self.__initHead__(), Qt.AlignTop)
        grid.addLayout(self.__initContent__())
        grid.addLayout(self.__initTail__(), Qt.AlignBottom)

    def __initHead__(self):
        self._searchEdit = LineEdit()
        self._searchBtn = PushButton('Search', ButtonStyle.Primary,
                                     iconUrl=getPackagePath() + "/resource/svg/search.svg")

        layout = createHBoxLayout([self._searchEdit, self._searchBtn])
        return layout

    def __initTail__(self):
        self._trackQualityComboBox = ComboBox([])
        self._videoQualityComboBox = ComboBox([])

        self._prePageBtn = PushButton('', ButtonStyle.PrePage)
        self._nextPageBtn = PushButton('', ButtonStyle.NextPage)
        self._pageIndexEdit = LineEdit('')

        self._downloadBtn = PushButton('Download', ButtonStyle.Primary)

        layout = QHBoxLayout()
        layout.addWidget(Label('Track:'))
        layout.addWidget(self._trackQualityComboBox)
        layout.addWidget(Label('Video:'))
        layout.addWidget(self._videoQualityComboBox)
        layout.addStretch(1)
        layout.addWidget(self._prePageBtn)
        layout.addWidget(self._pageIndexEdit)
        layout.addWidget(self._nextPageBtn)
        layout.addWidget(self._downloadBtn)
        return layout

    def __initContent__(self):
        self._tabWidget = QTabWidget(self)
        self._tabWidget.addTab(self.__initAlbumTable__(), "ALBUM")
        self._tabWidget.addTab(self.__initTrackTable__(), "TRACK")

        layout = QVBoxLayout()
        layout.addWidget(self._tabWidget)
        return layout

    def __initAlbumTable__(self):
        columnHeads = ['#', 'Q', 'Title', 'Artists', 'Release', 'Duration']
        self._albumTable = TableWidget(columnHeads, self._rowCount)
        return self._albumTable

    def setAlbumTableItems(self, albums: list[tidal_dl.model.Album]):
        # self._albumTable.ro
        for index, item in enumerate(albums):
            self._albumTable.addItem(index, 0, str(index + 1))
            self._albumTable.addItem(index, 1, item.audioQuality)
            self._albumTable.addItem(index, 2, item.title)
            self._albumTable.addItem(index, 3, item.artists[0].name)
            self._albumTable.addItem(index, 4, str(item.releaseDate))
            self._albumTable.addItem(index, 5, str(item.duration))

    def __initTrackTable__(self):
        columnHeads = ['', '#', 'Img', 'Title', 'Quality', 'Artists', 'Album']
        self._trackTable = TableWidget(columnHeads)
        return self._trackTable

    def getSearchText(self):
        return self._searchEdit.text()

    def setPageIndex(self, index):
        self._pageIndexEdit.setText(str(index))

    def getPageIndex(self):
        return int(self._pageIndexEdit.text())

    def getSelectedTabIndex(self):
        return self._tabWidget.currentIndex()

    def setTrackQualityItems(self, items:list):
        self._trackQualityComboBox.setItems(items)

    def setVideoQualityItems(self, items: list):
        self._videoQualityComboBox.setItems(items)

    def getTrackQualityText(self):
        return self._trackQualityComboBox.currentText()

    def getVideoQualityText(self):
        return self._videoQualityComboBox.currentText()

    def connectButton(self, name: str, func):
        if name == 'search':
            self._searchBtn.clicked.connect(func)
        elif name == 'prePage':
            self._prePageBtn.clicked.connect(func)
        elif name == 'nextPage':
            self._nextPageBtn.clicked.connect(func)
        elif name == 'download':
            self._downloadBtn.clicked.connect(func)
