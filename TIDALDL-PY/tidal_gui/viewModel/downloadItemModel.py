#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  downloadItemModel.py
@Date    :  2021/10/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""

import os
from abc import ABC, ABCMeta
from enum import Enum
from pickle import FALSE
from aigpy.downloadHelper import UserProgress
import aigpy.stringHelper

from tidal_dl.model import Track
from tidal_dl.util import downloadTrack, downloadVideo, getArtistsNames, setMetaData
from tidal_gui.view.downloadItemView import DownloadItemView
from tidal_gui.viewModel.viewModel import ViewModel


class DownloadStatus(Enum):
    Wait = 0,
    Running = 1,
    Finish = 2,
    Error = 3,
    Cancel = 4,


_endStatus_ = [DownloadStatus.Finish, DownloadStatus.Error, DownloadStatus.Cancel]


class Progress(UserProgress):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def updateCurNum(self):
        self.model.update(self.curNum, self.maxNum)

    def updateMaxNum(self):
        pass


class DownloadItemModel(ViewModel):
    def __init__(self, index, data, basePath):
        super(DownloadItemModel, self).__init__()
        self.view = DownloadItemView()
        self.data = data
        self.basePath = basePath
        self.isTrack = isinstance(data, Track)
        self.progress = Progress(self)
        self.__setStatus__(DownloadStatus.Wait)

        if self.isTrack:
            self.__initTrack__(index)
        else:
            self.__initVideo__(index)

    def __setStatus__(self, status: DownloadStatus, desc: str = ''):
        self.status = status
        if desc == '':
            self.view.setAction(status.name)
        else:
            self.view.setAction(status.name + '-' + desc)

    def __setErrStatus__(self, errmsg: str):
        self.status = DownloadStatus.Error
        self.view.setAction(self.status.name)
        self.view.setErrmsg(errmsg)

    def __initTrack__(self, index):
        title = self.data.title
        own = self.data.album.title
        self.view.setLabel(index, title, own)

    def __initVideo__(self, index):
        title = self.data.title
        own = getArtistsNames(self.data.artists)
        self.view.setLabel(index, title, own)

    def update(self, curNum, maxNum):
        per = curNum * 100 / maxNum
        self.view.setProgress(per)

    def isInWait(self):
        return self.status == DownloadStatus.Wait

    def stopDownload(self):
        if self.status not in _endStatus_:
            self.__setStatus__(DownloadStatus.Cancel)

    def retry(self):
        self.__setStatus__(DownloadStatus.Wait)

    def download(self):
        self.__setStatus__(DownloadStatus.Running)

        if self.isTrack:
            check, msg = downloadTrack(self.data, self.data.album, self.data.playlist, self.progress)
        else:
            check, msg = downloadVideo(self.data)
            
        if check is False:
            self.__setErrStatus__(msg)
        else:
            self.__setStatus__(DownloadStatus.Finish)

        self.view.setProgress(100)
        self.__setStatus__(DownloadStatus.Finish)

