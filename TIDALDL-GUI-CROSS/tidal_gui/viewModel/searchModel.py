#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  searchModel.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import _thread
import threading

import aigpy.stringHelper
import tidal_dl
from PyQt5.QtCore import pyqtSignal
from aigpy.modelHelper import ModelBase
from tidal_dl import Type
from tidal_dl.model import Album, SearchResult

from tidal_gui.tidalImp import tidalImp
from tidal_gui.view.searchView import SearchView
from tidal_gui.viewModel.viewModel import ViewModel


class SearchModel(ViewModel):
    SIGNAL_ADD_TASKITEM = pyqtSignal(ModelBase)

    def __init__(self):
        super(SearchModel, self).__init__()
        self._lock = threading.Lock()
        self._resultData = SearchResult()
        self.view = SearchView()
        self.view.setPageIndex(1)
        self.view.connectButton('search', self.__search__)
        self.view.connectButton('prePage', self.__searchPrePage__)
        self.view.connectButton('nextPage', self.__searchNextPage__)
        self.view.connectButton('download', self.__download__)
        self.view.connectTab(self.__search__)

    def __startThread__(self):
        def __thread_search__(model: SearchModel):
            typeIndex = model.view.getSelectedTabIndex()
            pageIndex = model.view.getPageIndex()
            searchText = model.view.getSearchText()

            limit = 20
            offset = (pageIndex - 1) * limit
            stype = tidal_dl.Type(typeIndex)
            msg, model._resultData = tidalImp.search(searchText, stype, offset, limit)

            if not aigpy.stringHelper.isNull(msg):
                # errmessage
                model._lock.release()
                return

            model.view.setTableItems(stype, offset, model._resultData)
            model._lock.release()

        _thread.start_new_thread(__thread_search__, (self,))

    def __search__(self):
        if not self._lock.acquire(False):
            return
        self.view.setPageIndex(1)
        self.__startThread__()

    def __searchNextPage__(self):
        if not self._lock.acquire(False):
            return
        self.view.setPageIndex(self.view.getPageIndex() + 1)
        self.__startThread__()

    def __searchPrePage__(self):
        if not self._lock.acquire(False):
            return
        index = self.view.getPageIndex() - 1
        if index < 1:
            index = 1
        self.view.setPageIndex(index)
        self.__startThread__()

    def __download__(self):
        typeIndex = self.view.getSelectedTabIndex()
        stype = tidal_dl.Type(typeIndex)
        index = self.view.getSelectedTableIndex(stype)
        if index <= 0:
            pass

        data = None
        if stype == Type.Album:
            data = self._resultData.albums.items[index]
        elif stype == Type.Track:
            data = self._resultData.tracks.items[index]
        elif stype == Type.Video:
            data = self._resultData.videos.items[index]
        elif stype == Type.Playlist:
            data = self._resultData.playlists.items[index]

        if data is not None:
            self.SIGNAL_ADD_TASKITEM.emit(data)
