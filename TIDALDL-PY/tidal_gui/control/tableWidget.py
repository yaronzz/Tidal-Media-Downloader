#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  tableWidget.py
@Date    :  2021/8/18
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import threading

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView

from tidal_gui.control.label import Label, LabelStyle


class TableWidget(QTableWidget):
    def __init__(self, columnNames: list, rowCount: int = 20):
        super(TableWidget, self).__init__()
        self.setColumnCount(len(columnNames))
        self.setRowCount(rowCount)

        self._lock = threading.Lock()
        self._netManager = QNetworkAccessManager()

        self.columnAligns = []

        for index, name in enumerate(columnNames):
            item = QTableWidgetItem(name)

            align = Qt.AlignLeft | Qt.AlignVCenter
            if name == '#' or name == ' ':
                align = Qt.AlignCenter

            self.columnAligns.append(align)
            item.setTextAlignment(align)
            self.setHorizontalHeaderItem(index, item)

        for index in range(0, rowCount):
            self.setRowHeight(index, 50)

        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setFocusPolicy(Qt.NoFocus)

    def changeRowCount(self, rows: int):
        if rows != self.rowCount():
            self.setRowCount(rows)
            for index in range(0, rows):
                self.setRowHeight(index, 50)

    def addItem(self, rowIdx: int, colIdx: int, text):
        if isinstance(text, str):
            item = QTableWidgetItem(text)
            item.setTextAlignment(self.columnAligns[colIdx])
            self.setItem(rowIdx, colIdx, item)
        elif isinstance(text, QUrl):
            self.__addPicItem__(rowIdx, colIdx, text)

    def __picDownload__(self, rowIdx, colIdx):
        reply = self.sender()
        data = reply.readAll()
        if data.size() <= 0:
            return

        pic = QPixmap()
        pic.loadFromData(data)

        self._lock.acquire()
        self.cellWidget(rowIdx, colIdx).setPixmap(pic.scaled(32, 32))
        self._lock.release()

        reply.deleteLater()

    def __addPicItem__(self, rowIdx: int, colIdx: int, url: QUrl):
        icon = Label('', LabelStyle.Icon)
        icon.setAlignment(Qt.AlignCenter)

        self.setCellWidget(rowIdx, colIdx, icon)

        reply = self._netManager.get(QNetworkRequest(url))
        reply.finished.connect(lambda: self.__picDownload__(rowIdx, colIdx))

    def addWidgetItem(self, rowIdx: int, colIdx: int, widget):
        self.setCellWidget(rowIdx, colIdx, widget)
