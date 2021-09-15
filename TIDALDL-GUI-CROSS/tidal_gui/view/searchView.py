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
from tidal_dl import Type

from tidal_gui.control.comboBox import ComboBox
from tidal_gui.control.label import Label
from tidal_gui.control.layout import createHBoxLayout
from tidal_gui.control.lineEdit import LineEdit
from tidal_gui.control.pushButton import PushButton
from tidal_gui.control.tableView import TableView
from tidal_gui.control.tableWidget import TableWidget
from tidal_gui.style import ButtonStyle
from tidal_gui.theme import getPackagePath
from tidal_gui.tidalImp import tidalImp


class SearchView(QWidget):
    def __init__(self):
        super(SearchView, self).__init__()
        self._rowCount = 20
        self._table = {}
        self.__initView__()
        self._searchEdit.setFocus()
        self._searchBtn.setDefault(True)

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
        self._tabWidget.addTab(self.__initTable__(Type.Album), "ALBUM")
        self._tabWidget.addTab(self.__initTable__(Type.Track), "TRACK")
        self._tabWidget.addTab(self.__initTable__(Type.Video), "VIDEO")
        self._tabWidget.addTab(self.__initTable__(Type.Playlist), "PLAYLIST")

        layout = QVBoxLayout()
        layout.addWidget(self._tabWidget)
        return layout

    def __initTable__(self, stype: Type):
        if stype == Type.Album:
            columnHeads = ['#', ' ', 'Title', 'Artists', 'Release', 'Duration']
            self._table[stype] = TableWidget(columnHeads)
            self._table[stype].setColumnWidth(0, 50)
            self._table[stype].setColumnWidth(1, 60)
            self._table[stype].setColumnWidth(2, 400)
            self._table[stype].setColumnWidth(3, 200)
        elif stype == Type.Track:
            columnHeads = ['#', ' ', 'Title', 'Album', 'Artists', 'Duration']
            self._table[stype] = TableWidget(columnHeads)
            self._table[stype].setColumnWidth(0, 50)
            self._table[stype].setColumnWidth(1, 60)
            self._table[stype].setColumnWidth(2, 400)
            self._table[stype].setColumnWidth(3, 200)
            self._table[stype].setColumnWidth(4, 200)
        elif stype == Type.Video:
            columnHeads = ['#', ' ', 'Title', 'Artists', 'Duration']
            self._table[stype] = TableWidget(columnHeads)
            self._table[stype].setColumnWidth(0, 50)
            self._table[stype].setColumnWidth(1, 60)
            self._table[stype].setColumnWidth(2, 400)
            self._table[stype].setColumnWidth(3, 200)
            self._table[stype].setColumnWidth(4, 200)
        elif stype == Type.Playlist:
            columnHeads = ['#', 'Title', 'Artist', 'Duration']
            self._table[stype] = TableWidget(columnHeads)
            self._table[stype].setColumnWidth(0, 50)
            self._table[stype].setColumnWidth(1, 400)
            self._table[stype].setColumnWidth(2, 200)
            self._table[stype].setColumnWidth(3, 200)
        return self._table[stype]

    def setTableItems(self, stype: Type, indexOffset: int, result: tidal_dl.model.SearchResult):
        if stype == Type.Album:
            items = result.albums.items
            self._table[stype].changeRowCount(len(items))
            for index, item in enumerate(items):
                self._table[stype].addItem(index, 0, str(index + 1 + indexOffset))
                self._table[stype].addItem(index, 1, tidalImp.getFlag(item, Type.Album, True))
                self._table[stype].addItem(index, 2, item.title)
                self._table[stype].addItem(index, 3, item.artists[0].name)
                self._table[stype].addItem(index, 4, str(item.releaseDate))
                self._table[stype].addItem(index, 5, tidalImp.getDurationString(item.duration))
        elif stype == Type.Track:
            items = result.tracks.items
            self._table[stype].changeRowCount(len(items))
            for index, item in enumerate(items):
                self._table[stype].addItem(index, 0, str(index + 1 + indexOffset))
                self._table[stype].addItem(index, 1, tidalImp.getFlag(item, Type.Track, True))
                self._table[stype].addItem(index, 2, item.title)
                self._table[stype].addItem(index, 3, item.album.title)
                self._table[stype].addItem(index, 4, item.artists[0].name)
                self._table[stype].addItem(index, 5, tidalImp.getDurationString(item.duration))
        elif stype == Type.Video:
            items = result.videos.items
            self._table[stype].changeRowCount(len(items))
            for index, item in enumerate(items):
                self._table[stype].addItem(index, 0, str(index + 1 + indexOffset))
                self._table[stype].addItem(index, 1, tidalImp.getFlag(item, Type.Video, True))
                self._table[stype].addItem(index, 2, item.title)
                self._table[stype].addItem(index, 3, item.artists[0].name)
                self._table[stype].addItem(index, 4, tidalImp.getDurationString(item.duration))
        elif stype == Type.Playlist:
            items = result.playlists.items
            self._table[stype].changeRowCount(len(items))
            for index, item in enumerate(items):
                self._table[stype].addItem(index, 0, str(index + 1 + indexOffset))
                self._table[stype].addItem(index, 1, item.title)
                self._table[stype].addItem(index, 2, '')
                self._table[stype].addItem(index, 3, tidalImp.getDurationString(item.duration))
        self._table[stype].viewport().update()

    def getSearchText(self):
        return self._searchEdit.text()

    def setPageIndex(self, index):
        self._pageIndexEdit.setText(str(index))

    def getPageIndex(self):
        return int(self._pageIndexEdit.text())

    def getSelectedTabIndex(self):
        return self._tabWidget.currentIndex()

    def getSelectedTableIndex(self, stype: Type):
        array = self._table[stype].selectedIndexes()
        if len(array) <= 0:
            return -1
        return array[0].row()

    def setTrackQualityItems(self, items: list):
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
            self._searchEdit.returnPressed.connect(func)
        elif name == 'prePage':
            self._prePageBtn.clicked.connect(func)
        elif name == 'nextPage':
            self._nextPageBtn.clicked.connect(func)
        elif name == 'download':
            self._downloadBtn.clicked.connect(func)

    def connectTab(self, func):
        self._tabWidget.currentChanged.connect(func)
