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
from tidal_gui.view.searchView import SearchView
from tidal_gui.viewModel.viewModel import ViewModel


class SearchModel(ViewModel):
    def __init__(self):
        super(SearchModel, self).__init__()
        self.view = SearchView()
