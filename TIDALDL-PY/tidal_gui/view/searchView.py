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
import threading

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget

import tidal_dl.model
from tidal_dl import Type
from tidal_dl.util import API, getDurationString
from tidal_gui.control.comboBox import ComboBox
from tidal_gui.control.label import Label
from tidal_gui.control.lineEdit import LineEdit
from tidal_gui.control.pushButton import PushButton
from tidal_gui.control.tableWidget import TableWidget
from tidal_gui.style import ButtonStyle, LabelStyle
from tidal_gui.theme import getResourcePath


class SearchView(QWidget):
    def __init__(self):
        super(SearchView, self).__init__()
        self._rowCount = 20
        self._table = {}
        self._lock = threading.Lock()
        self.__initView__()
        self._searchEdit.setFocus()

    def __initView__(self):
        grid = QVBoxLayout(self)
        grid.addLayout(self.__initHead__(), Qt.AlignTop)
        grid.addLayout(self.__initContent__())
        grid.addLayout(self.__initTail__(), Qt.AlignBottom)

    def __initHead__(self):
        self._searchEdit = LineEdit(iconUrl=getResourcePath() + "/svg/search2.svg")
        self._searchErrLabel = Label('', LabelStyle.SearchErr)
        self._searchErrLabel.hide()
        layout = QVBoxLayout()
        layout.addWidget(self._searchEdit)
        layout.addWidget(self._searchErrLabel)
        layout.setContentsMargins(0, 0, 0, 5)
        return layout

    def __initTail__(self):
        self._trackQualityComboBox = ComboBox([], 150)
        self._videoQualityComboBox = ComboBox([], 150)

        self._prePageBtn = PushButton('', ButtonStyle.PrePage)
        self._nextPageBtn = PushButton('', ButtonStyle.NextPage)

        self._pageIndexEdit = LineEdit('')
        self._pageIndexEdit.setAlignment(Qt.AlignCenter)
        self._pageIndexEdit.setEnabled(False)

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
        columnHeads = []
        columnWidths = []
        if stype == Type.Album:
            columnHeads = ['#', ' ', ' ', 'Title', 'Artists', 'Release', 'Duration']
            columnWidths = [50, 60, 60, 400, 200, 200]
        elif stype == Type.Track:
            columnHeads = ['#', ' ', 'Title', 'Album', 'Artists', 'Duration']
            columnWidths = [50, 60, 400, 200, 200]
        elif stype == Type.Video:
            columnHeads = ['#', ' ', ' ', 'Title', 'Artists', 'Duration']
            columnWidths = [50, 60, 60, 400, 200, 200]
        elif stype == Type.Playlist:
            columnHeads = ['#', ' ', 'Title', 'Artist', 'Duration']
            columnWidths = [50, 60, 400, 200, 200]

        self._table[stype] = TableWidget(columnHeads, self._rowCount)
        for index, width in enumerate(columnWidths):
            self._table[stype].setColumnWidth(index, width)

        return self._table[stype]

    def __clearTableRowItems__(self, stype: Type, fromIndex: int):
        endIndex = self._rowCount - 1
        columnNum = self._table[stype].columnCount()
        while fromIndex <= endIndex:
            for colIdx in range(0, columnNum):
                self._table[stype].addItem(fromIndex, colIdx, '')
            fromIndex += 1

    def setTableItems(self, stype: Type, indexOffset: int, result: tidal_dl.model.SearchResult):
        if stype == Type.Album:
            items = result.albums.items
            datas = []
            for index, item in enumerate(items):
                rowData = [str(index + 1 + indexOffset),
                           QUrl(API.getCoverUrl(item.cover)),
                           API.getFlag(item, Type.Album, True),
                           item.title,
                           item.artists[0].name,
                           str(item.releaseDate),
                           getDurationString(item.duration)]
                datas.append(rowData)

        elif stype == Type.Track:
            items = result.tracks.items
            datas = []
            for index, item in enumerate(items):
                rowData = [str(index + 1 + indexOffset),
                           API.getFlag(item, Type.Track, True),
                           item.title,
                           item.album.title,
                           item.artists[0].name,
                           getDurationString(item.duration)]
                datas.append(rowData)

        elif stype == Type.Video:
            items = result.videos.items
            datas = []
            for index, item in enumerate(items):
                rowData = [str(index + 1 + indexOffset),
                           QUrl(API.getCoverUrl(item.imageID)),
                           API.getFlag(item, Type.Video, True),
                           item.title,
                           item.artists[0].name,
                           getDurationString(item.duration)]
                datas.append(rowData)

        elif stype == Type.Playlist:
            items = result.playlists.items
            datas = []
            for index, item in enumerate(items):
                rowData = [str(index + 1 + indexOffset),
                           QUrl(API.getCoverUrl(item.squareImage)),
                           item.title,
                           '',
                           getDurationString(item.duration)]
                datas.append(rowData)

        for index, rowData in enumerate(datas):
            for colIdx, obj in enumerate(rowData):
                self._table[stype].addItem(index, colIdx, obj)

        self.__clearTableRowItems__(stype, len(items))
        self._table[stype].viewport().update()

    def getSearchText(self):
        return self._searchEdit.text()

    def setSearchErrmsg(self, text: str):
        self._searchErrLabel.setText(text)
        if text != '':
            self._searchErrLabel.show()
        else:
            self._searchErrLabel.hide()

    def setPageIndex(self, index, sum):
        self._pageIndexEdit.setText(str(index) + '/' + str(sum))

    def getPageIndex(self) -> (int, int):
        nums = self._pageIndexEdit.text().split('/')
        return int(nums[0]), int(nums[1])

    def getSelectedTabIndex(self):
        return self._tabWidget.currentIndex()

    def getSelectedTableIndex(self, stype: Type):
        array = self._table[stype].selectedIndexes()
        if len(array) <= 0:
            return -1
        return array[0].row()

    def setTrackQualityItems(self, items: list, curItem = None):
        self._trackQualityComboBox.setItems(items)
        if curItem is not None:
            self._trackQualityComboBox.setCurrentText(curItem)

    def setVideoQualityItems(self, items: list, curItem=None):
        self._videoQualityComboBox.setItems(items)
        if curItem is not None:
            self._videoQualityComboBox.setCurrentText(curItem)

    def getTrackQualityText(self):
        return self._trackQualityComboBox.currentText()

    def getVideoQualityText(self):
        return self._videoQualityComboBox.currentText()

    def connectButton(self, name: str, func):
        if name == 'search':
            self._searchEdit.returnPressed.connect(func)
        elif name == 'prePage':
            self._prePageBtn.clicked.connect(func)
        elif name == 'nextPage':
            self._nextPageBtn.clicked.connect(func)
        elif name == 'download':
            self._downloadBtn.clicked.connect(func)

    def connectTab(self, func):
        self._tabWidget.currentChanged.connect(func)
    
    def connectQualityComboBox(self, name: str, func):
        if name == 'track':
            self._trackQualityComboBox.currentIndexChanged.connect(func)
        else:
            self._videoQualityComboBox.currentIndexChanged.connect(func)
