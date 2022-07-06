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
import sys
import _thread
import importlib

from tidal_dl.events import *
from tidal_dl.settings import *
from tidal_dl.printf import *

enableGui = False
try:
    params = importlib.import_module('PyQt5')
    params = importlib.import_module('qt_material')
    enableGui = True
except Exception as e:
    pass

if enableGui:
    from PyQt5.QtCore import Qt
    from PyQt5.QtCore import pyqtSignal
    from PyQt5 import QtWidgets
    from qt_material import apply_stylesheet

    class MainView(QtWidgets.QWidget):
        s_downloadEnd = pyqtSignal(str, bool, str)

        def __init__(self, ) -> None:
            super().__init__()
            self.initView()
            self.setMinimumSize(600, 500)
            self.setWindowTitle("Tidal-dl")
        
        def __info__(self, msg):
            QtWidgets.QMessageBox.information(self, 
                                            'Info', 
                                            msg,
                                            QtWidgets.QMessageBox.Yes)
        
        def initView(self):
            self.c_lineSearch = QtWidgets.QLineEdit()
            self.c_btnSearch = QtWidgets.QPushButton("Search")
            self.c_btnDownload = QtWidgets.QPushButton("Download")

            self.m_supportType = [Type.Album, Type.Playlist, Type.Track, Type.Video]
            self.c_combType = QtWidgets.QComboBox()
            for item in self.m_supportType:
                self.c_combType.addItem(item.name, item)

            columnNames = ['#', 'Title', 'Artists', 'Quality']
            self.c_tableInfo = QtWidgets.QTableWidget()
            self.c_tableInfo.setColumnCount(len(columnNames))
            self.c_tableInfo.setRowCount(0)
            self.c_tableInfo.setShowGrid(False)
            self.c_tableInfo.verticalHeader().setVisible(False)
            self.c_tableInfo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.c_tableInfo.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.c_tableInfo.horizontalHeader().setStretchLastSection(True)
            self.c_tableInfo.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.c_tableInfo.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.c_tableInfo.setFocusPolicy(Qt.NoFocus)
            for index, name in enumerate(columnNames):
                item = QtWidgets.QTableWidgetItem(name)
                self.c_tableInfo.setHorizontalHeaderItem(index, item)

            self.lineGrid = QtWidgets.QHBoxLayout()
            self.lineGrid.addWidget(self.c_combType)
            self.lineGrid.addWidget(self.c_lineSearch)
            self.lineGrid.addWidget(self.c_btnSearch)

            self.mainGrid = QtWidgets.QVBoxLayout(self)
            self.mainGrid.addLayout(self.lineGrid)
            self.mainGrid.addWidget(self.c_tableInfo)
            self.mainGrid.addWidget(self.c_btnDownload)

            self.c_btnSearch.clicked.connect(self.search)
            self.c_btnDownload.clicked.connect(self.download)
            self.s_downloadEnd.connect(self.downloadEnd)

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

            self.c_tableInfo.setRowCount(len(self.s_array))
            for index, item in enumerate(self.s_array):
                self.addItem(index, 0, str(index + 1))
                if self.s_type in [Type.Album, Type.Track]:
                    self.addItem(index, 1, item.title)
                    self.addItem(index, 2, TIDAL_API.getArtistsName(item.artists))
                    self.addItem(index, 3, item.audioQuality)
                elif self.s_type in [Type.Video]:
                    self.addItem(index, 1, item.title)
                    self.addItem(index, 2, TIDAL_API.getArtistsName(item.artists))
                    self.addItem(index, 3, item.quality)
                elif self.s_type in [Type.Playlist]:
                    self.addItem(index, 1, item.title)
                    self.addItem(index, 2, '')
                    self.addItem(index, 3, '')
            self.c_tableInfo.viewport().update()

        def download(self):
            index = self.c_tableInfo.currentIndex().row()
            if index < 0:
                self.__info__('Please select a row first.')
                return

            self.c_btnDownload.setEnabled(False)
            self.c_btnDownload.setText(f"Downloading [{self.s_array[index].title}]...")

            def __thread_download__(model: MainView):
                try:
                    type = model.s_type
                    item = model.s_array[index]
                    start_type(type, item)
                    model.s_downloadEnd.emit(item.title, True, '')
                except Exception as e:
                    model.s_downloadEnd.emit(item.title, False, str(e))

            _thread.start_new_thread(__thread_download__, (self, ))

        def downloadEnd(self, title, result, msg):
            self.c_btnDownload.setEnabled(True)
            self.c_btnDownload.setText(f"Download")

            if result:
                self.__info__(f'Download [{title}] finish')
            else:
                self.__info__(f'Download [{title}] failed:{msg}')

        def checkLogin(self):
            if not loginByConfig():
                self.__info__('Login failed. Please log in using the command line first.')


    def startGui():
        app = QtWidgets.QApplication(sys.argv)
        apply_stylesheet(app, theme='dark_blue.xml')

        window = MainView()
        window.show()
        window.checkLogin()

        app.exec_()
else:
    def startGui():
        Printf.err("Not support gui. Please type: `pip3 install PyQt5 qt_material`")

if __name__ == '__main__':
    SETTINGS.read(getProfilePath())
    TOKEN.read(getTokenPath())
    startGui()
