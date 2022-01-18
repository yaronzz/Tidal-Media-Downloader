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
import aigpy
from abc import ABC, ABCMeta
from enum import Enum
from pickle import FALSE
from aigpy.downloadHelper import UserProgress
import aigpy.stringHelper
from PyQt5.QtCore import pyqtSignal

from tidal_dl.model import Track
from tidal_dl.util import downloadTrack, downloadVideo, getArtistsNames, setMetaData
from tidal_gui.view.downloadItemView import DownloadItemView
from tidal_gui.viewModel.viewModel import ViewModel


class DownloadStatus(Enum):
    WAIT = 0,
    RUNNING = 1,
    SUCCESS = 2,
    ERROR = 3,
    CANCEL = 4,


_endStatus_ = [DownloadStatus.SUCCESS, DownloadStatus.ERROR, DownloadStatus.CANCEL]


class Progress(UserProgress):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.curStr = ''
        self.maxStr = ''

    def __toMBStr__(self, num):
        size = aigpy.memory.convert(num, aigpy.memory.Unit.BYTE, aigpy.memory.Unit.MB)
        return str(round(size, 2)) + ' MB'

    def updateCurNum(self):
        per = self.curNum * 100 / self.maxNum
        self.curStr = self.__toMBStr__(self.curNum)
        self.model.SIGNAL_REFRESH_VIEW.emit('updateCurNum', {'per': per,
                                                             'curStr': self.curStr,
                                                             'maxStr': self.maxStr})

    def updateMaxNum(self):
        self.maxStr = self.__toMBStr__(self.maxNum)
        
    def updateStream(self, stream):
        self.model.SIGNAL_REFRESH_VIEW.emit('updateStream', {'stream': stream})


class DownloadItemModel(ViewModel):
    SIGNAL_END = pyqtSignal(DownloadStatus)
    
    def __init__(self, index, data, basePath):
        super(DownloadItemModel, self).__init__()
        self.view = DownloadItemView()
        self.data = data
        self.basePath = basePath
        self.isTrack = isinstance(data, Track)
        self.progress = Progress(self)
        self.__setStatus__(DownloadStatus.WAIT)

        if self.isTrack:
            self.__initTrack__(index)
        else:
            self.__initVideo__(index)

        self.SIGNAL_REFRESH_VIEW.connect(self.__refresh__)

    def __refresh__(self, stype: str, object):
        if stype == "updateCurNum":
            per = object['per']
            curStr = object['curStr']
            maxStr = object['maxStr']
            self.view.setSize(curStr, maxStr)
            self.view.setProgress(per)
        elif stype == "updateStream":
            codec = object['stream'].codec
            self.view.setCodec(codec)


    def __setStatus__(self, status: DownloadStatus, desc: str = ''):
        self.status = status
        if desc == '':
            self.view.setAction(status.name)
        else:
            self.view.setAction(status.name + '-' + desc)
        if status in _endStatus_:
            self.SIGNAL_END.emit(status)
        

    def __setErrStatus__(self, errmsg: str):
        self.view.setErrmsg(errmsg)
        self.__setStatus__(DownloadStatus.ERROR)

    def __initTrack__(self, index):
        title = self.data.title
        own = self.data.album.title
        self.view.setLabel(index, title, own)

    def __initVideo__(self, index):
        title = self.data.title
        own = getArtistsNames(self.data.artists)
        self.view.setLabel(index, title, own)

    def isInWait(self):
        return self.status == DownloadStatus.WAIT

    def stopDownload(self):
        if self.status not in _endStatus_:
            self.__setStatus__(DownloadStatus.CANCEL)

    def retry(self):
        if self.status in [DownloadStatus.ERROR, DownloadStatus.CANCEL]:
            self.__setStatus__(DownloadStatus.WAIT)

    def download(self):
        self.__setStatus__(DownloadStatus.RUNNING)

        if self.isTrack:
            check, msg = downloadTrack(self.data, self.data.album, self.data.playlist, self.progress)
        else:
            check, msg = downloadVideo(self.data)

        if check is False:
            self.__setErrStatus__(msg)
            return

        self.view.setProgress(100)
        self.__setStatus__(DownloadStatus.SUCCESS)
