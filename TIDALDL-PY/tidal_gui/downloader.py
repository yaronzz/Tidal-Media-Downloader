#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  downloader.py
@Date    :  2021/09/15
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""
import time

from PyQt5.Qt import QThread

from tidal_gui.viewModel.taskModel import TaskModel


class DownloaderImp(QThread):
    def __init__(self):
        super(DownloaderImp, self).__init__()
        self._taskModel = None

    def run(self):
        print('DownloadImp start...')
        while not self.isInterruptionRequested():
            if self._taskModel is not None:
                item = self._taskModel.getWaitDownloadItem()
                if item is not None:
                    item.download()
            time.sleep(1)
        print('DownloadImp stop...')

    def setTaskModel(self, model: TaskModel):
        self._taskModel = model

    def stop(self):
        self.requestInterruption()
        self.wait()


downloadImp = DownloaderImp()
