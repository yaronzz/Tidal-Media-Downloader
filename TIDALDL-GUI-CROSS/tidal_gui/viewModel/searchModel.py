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

from tidal_gui.tidalImp import tidalImp
from tidal_gui.view.searchView import SearchView
from tidal_gui.viewModel.viewModel import ViewModel


class SearchModel(ViewModel):
    def __init__(self):
        super(SearchModel, self).__init__()
        self._lock = threading.Lock()
        self.view = SearchView()
        self.view.setPageIndex(1)
        self.view.connectButton('search', self.__search__)

    def __search__(self):
        if not self._lock.acquire(False):
            return

        def __thread_search__(model: SearchModel):
            typeIndex = model.view.getSelectedTabIndex()
            pageIndex = model.view.getPageIndex()
            searchText = model.view.getSearchText()

            limit = 20
            msg, data = tidalImp.search(searchText, tidal_dl.Type(typeIndex), (pageIndex - 1) * limit, limit)
            if aigpy.stringHelper.isNull(msg) and data is not None:
                model.view.setAlbumTableItems(data.albums.items)
            model._lock.release()

        _thread.start_new_thread(__thread_search__, (self,))
