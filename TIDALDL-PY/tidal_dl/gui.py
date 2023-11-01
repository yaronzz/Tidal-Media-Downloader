#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  test.py
@Date    :  2022/03/28
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import importlib
import sys
import _thread

from events import *
from printf import *


def enableGui():
    try:
        importlib.import_module('PyQt5')
        importlib.import_module('qt_material')
        return True
    except Exception as e:
        return False


if not enableGui():
    def startGui():
        Printf.err("Not support gui. Please type: `pip3 install PyQt5 qt_material`")
else:
    from PyQt5.QtCore import Qt, QObject
    from PyQt5.QtGui import QTextCursor, QKeyEvent
    from PyQt5.QtCore import pyqtSignal
    from PyQt5 import QtWidgets
    from qt_material import apply_stylesheet

    class EmittingStream(QObject):
        textWritten = pyqtSignal(str)

        def write(self, text):
            self.textWritten.emit(str(text))

    class MainView(QtWidgets.QWidget):
        s_downloadEnd = pyqtSignal(str, bool, str)

        def __init__(self, ) -> None:
            super().__init__()
            self.initView()
            self.setMinimumSize(800, 620)
            self.setWindowTitle("TIDAL-DL")

        def __info__(self, msg):
            QtWidgets.QMessageBox.information(self, 'Info', msg, QtWidgets.QMessageBox.Yes)

        def __output__(self, text):
            cursor = self.c_printTextEdit.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(text)
            self.c_printTextEdit.setTextCursor(cursor)
            self.c_printTextEdit.ensureCursorVisible()

        def initView(self):
            self.c_lineSearch = QtWidgets.QLineEdit()
            self.c_btnSearch = QtWidgets.QPushButton("Search")
            self.c_btnDownload = QtWidgets.QPushButton("Download")
            self.c_combType = QtWidgets.QComboBox()
            self.c_combTQuality = QtWidgets.QComboBox()
            self.c_combVQuality = QtWidgets.QComboBox()

            # Supported types for search
            self.m_supportType = [Type.Album, Type.Playlist, Type.Track, Type.Video, Type.Artist]
            for item in self.m_supportType:
                self.c_combType.addItem(item.name, item)

            for item in AudioQuality:
                self.c_combTQuality.addItem(item.name, item)
            for item in VideoQuality:
                self.c_combVQuality.addItem(item.name, item)
            self.c_combTQuality.setCurrentText(SETTINGS.audioQuality.name)
            self.c_combVQuality.setCurrentText(SETTINGS.videoQuality.name)

            # init table
            columnNames = ['#', 'Title', 'Artists', 'Quality']
            self.c_tableInfo = QtWidgets.QTableWidget()
            self.c_tableInfo.setColumnCount(len(columnNames))
            self.c_tableInfo.setRowCount(0)
            self.c_tableInfo.setShowGrid(False)
            self.c_tableInfo.verticalHeader().setVisible(False)
            self.c_tableInfo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.c_tableInfo.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            self.c_tableInfo.horizontalHeader().setStretchLastSection(True)
            self.c_tableInfo.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.c_tableInfo.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.c_tableInfo.setFocusPolicy(Qt.NoFocus)
            for index, name in enumerate(columnNames):
                item = QtWidgets.QTableWidgetItem(name)
                self.c_tableInfo.setHorizontalHeaderItem(index, item)

            # Create Tree View for playlists.
            self.tree_playlists = QtWidgets.QTreeWidget()
            self.tree_playlists.setAnimated(False)
            self.tree_playlists.setIndentation(20)
            self.tree_playlists.setSortingEnabled(True)
            self.tree_playlists.setFixedWidth(200)
            self.tree_playlists.setColumnCount(1)
            self.tree_playlists.setHeaderLabels(("User Playlists",))
            # self.tree_playlists.setColumnWidth(0, 100)
            self.tree_playlists.setContextMenuPolicy(Qt.CustomContextMenu)

            # print
            self.c_printTextEdit = QtWidgets.QTextEdit()
            self.c_printTextEdit.setReadOnly(True)
            self.c_printTextEdit.setFixedHeight(100)
            sys.stdout = EmittingStream(textWritten=self.__output__)
            sys.stderr = EmittingStream(textWritten=self.__output__)

            # layout
            self.lineGrid = QtWidgets.QHBoxLayout()
            self.lineGrid.addWidget(self.c_combType)
            self.lineGrid.addWidget(self.c_lineSearch)
            self.lineGrid.addWidget(self.c_btnSearch)

            self.line2Grid = QtWidgets.QHBoxLayout()
            self.line2Grid.addWidget(QtWidgets.QLabel("QUALITY:"))
            self.line2Grid.addWidget(self.c_combTQuality)
            self.line2Grid.addWidget(self.c_combVQuality)
            self.line2Grid.addStretch(4)
            self.line2Grid.addWidget(self.c_btnDownload)

            self.funcGrid = QtWidgets.QVBoxLayout()
            self.funcGrid.addLayout(self.lineGrid)
            self.funcGrid.addWidget(self.c_tableInfo)
            self.funcGrid.addLayout(self.line2Grid)
            self.funcGrid.addWidget(self.c_printTextEdit)

            self.mainGrid = QtWidgets.QHBoxLayout(self)
            self.mainGrid.addWidget(self.tree_playlists)
            self.mainGrid.addLayout(self.funcGrid)

            # connect
            self.c_btnSearch.clicked.connect(self.search)
            self.c_lineSearch.returnPressed.connect(self.search)
            self.c_btnDownload.clicked.connect(self.download)
            self.s_downloadEnd.connect(self.downloadEnd)
            self.c_combTQuality.currentIndexChanged.connect(self.changeTQuality)
            self.c_combVQuality.currentIndexChanged.connect(self.changeVQuality)
            self.tree_playlists.itemClicked.connect(self.__displayTracks__)

        def keyPressEvent(self, event: QKeyEvent):
            if event.modifiers() & Qt.MetaModifier and event.key() == Qt.Key_A:
                self.c_tableInfo.selectAll()

        def addItem(self, rowIdx: int, colIdx: int, text):
            if isinstance(text, str):
                item = QtWidgets.QTableWidgetItem(text)
                self.c_tableInfo.setItem(rowIdx, colIdx, item)

        def search(self):
            self.c_tableInfo.setRowCount(0)
            self.s_type = self.c_combType.currentData()
            self.s_text = self.c_lineSearch.text()

            if self.s_text.startswith('http'):
                tmpType, tmpId = TIDAL_API.parseUrl(self.s_text)
                if tmpType == Type.Null:
                    self.__info__('Url not support！')
                    return
                elif tmpType not in self.m_supportType:
                    self.__info__(f'Type[{tmpType.name}] not support！')
                    return

                tmpData = TIDAL_API.getTypeData(tmpId, tmpType)
                if tmpData is None:
                    self.__info__('Url is wrong!')
                    return
                self.s_type = tmpType
                self.s_array = [tmpData]
                self.s_result = None
                self.c_combType.setCurrentText(tmpType.name)
            else:
                self.s_result = TIDAL_API.search(self.s_text, self.s_type)
                self.s_array = TIDAL_API.getSearchResultItems(self.s_result, self.s_type)

            if len(self.s_array) <= 0:
                self.__info__('No result！')
                return

            self.setSearchResults(self.s_array, self.s_type)

        def setSearchResults(self, s_array, s_type):
            self.c_tableInfo.clearSelection()
            self.c_tableInfo.setRowCount(len(s_array))

            for index, item in enumerate(s_array):
                self.addItem(index, 0, str(index + 1))
                if s_type in [Type.Album, Type.Track]:
                    self.addItem(index, 1, item.title)
                    self.addItem(index, 2, TIDAL_API.getArtistsName(item.artists))
                    self.addItem(index, 3, item.audioQuality)
                elif s_type in [Type.Video]:
                    self.addItem(index, 1, item.title)
                    self.addItem(index, 2, TIDAL_API.getArtistsName(item.artists))
                    self.addItem(index, 3, item.quality)
                elif s_type in [Type.Playlist]:
                    self.addItem(index, 1, item.title)
                    self.addItem(index, 2, '')
                    self.addItem(index, 3, '')
                elif s_type in [Type.Artist]:
                    self.addItem(index, 1, item.name)
                    self.addItem(index, 2, '')
                    self.addItem(index, 3, '')
            self.c_tableInfo.viewport().update()

        def download(self):
            if self.c_tableInfo.selectionModel().hasSelection() == False:
                self.__info__('Please select a row first.')
                return

            rows = self.c_tableInfo.selectionModel().selectedRows()
            items = []
            for row in rows:
                items.append(self.s_array[row.row()])
            
            self.__downloadFunc__(items)
        
        def __downloadFunc__(self, items):
            self.c_btnDownload.setEnabled(False)

            def __thread_download__(model: MainView, items):
                itemTitle = ''
                type = model.s_type
                try:
                    for item in items:
                        if isinstance(item, Artist):
                            itemTitle = item.name
                        else:
                            itemTitle = item.title
                        start_type(type, item)
                    model.s_downloadEnd.emit('Download Success!', True, '')
                except Exception as e:
                    model.s_downloadEnd.emit(itemTitle, False, str(e))

            _thread.start_new_thread(__thread_download__, (self, items))

        def downloadEnd(self, title, result, msg):
            self.c_btnDownload.setEnabled(True)
            self.c_btnDownload.setText(f"Download")

            if result:
                self.__info__(f"Download finished.")
            else:
                self.__info__(f"Download '{title}' failed:{msg}")

        def checkLogin(self):
            if not loginByConfig():
                self.__info__('Login failed. Please log in using the command line first.')
            else:
                self.__showSelfPlaylists__()

        def changeTQuality(self, index):
            SETTINGS.audioQuality = self.c_combTQuality.itemData(index)
            SETTINGS.save()

        def changeVQuality(self, index):
            SETTINGS.videoQuality = self.c_combVQuality.itemData(index)
            SETTINGS.save()

        def __showSelfPlaylists__(self):
            playlists = TIDAL_API.getPlaylistSelf()

            for playlist in playlists:
                item = QtWidgets.QTreeWidgetItem(self.tree_playlists)
                item.setText(0, playlist.title)
                item.setText(1, str(playlist.numberOfTracks))
                item.setText(2, playlist.uuid)

        def __displayTracks__(self, item, column):
            tracks, videos = TIDAL_API.getItems(item.text(2), Type.Playlist)
            self.s_array = tracks
            self.s_type = Type.Track

            self.setSearchResults(tracks, Type.Track)

    def startGui():
        aigpy.cmd.enableColor(False)

        app = QtWidgets.QApplication(sys.argv)
        apply_stylesheet(app, theme='dark_blue.xml')

        window = MainView()
        window.show()
        window.checkLogin()

        app.exec_()

if __name__ == '__main__':
    SETTINGS.read(getProfilePath())
    TOKEN.read(getTokenPath())
    startGui()
