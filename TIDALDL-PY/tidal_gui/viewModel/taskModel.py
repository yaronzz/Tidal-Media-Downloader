#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  taskModel.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
from PyQt5.QtWidgets import QPushButton, QCheckBox, QWidget
from tidal_dl import Type
from tidal_dl.model import Album, Artist

from tidal_gui.control.layout import createHBoxLayout
from tidal_gui.view.taskView import TaskView, TaskListType
from tidal_gui.viewModel.taskItemModel import TaskItemModel
from tidal_gui.viewModel.viewModel import ViewModel
from tidal_gui.viewModel.downloadItemModel import DownloadItemModel


class TaskModel(ViewModel):
    def __init__(self):
        super(TaskModel, self).__init__()
        self.view = TaskView()
        
        self._listMap = {}
        for item in map(lambda typeItem: typeItem.name, TaskListType):
            self._listMap[item] = []
            
        self.test()
        
    def addTaskItem(self, data):
        item = TaskItemModel(data)
        self._listMap[TaskListType.Download.name].append(item)
        self.view.addItemView(TaskListType.Download, item.view)
        
    def getWaitDownloadItem(self) -> DownloadItemModel:
        for item in self._listMap[TaskListType.Download.name]:
            for downItem in item.downloadModelList:
                if downItem.isInWait():
                    return downItem
        return None
    
    def stopDownloadItem(self):
        for item in self._listMap[TaskListType.Download.name]:
            for downItem in item.downloadModelList:
                downItem.stopDownload()

    def test(self):
        ar = Artist()
        ar.name = 'yaron'
        ar.id = 110
        album = Album()
        album.artist = None
        album.artists = [ar]
        album.audioModes = ['STEREO']
        album.audioQuality = 'LOSSLESS'
        album.cover = '8203ff9a-47e3-49a0-9b44-a6dbbe9c9469'
        album.duration = 1140
        album.explicit = False
        album.id = 177748204
        album.numberOfTracks = 10
        album.numberOfVideos = 0
        album.numberOfVolumes = 1
        album.releaseDate = '2021-03-16'
        album.title = 'Love'
        album.type = 'ALBUM'
        album.version = None

        self.addTaskItem(album)
