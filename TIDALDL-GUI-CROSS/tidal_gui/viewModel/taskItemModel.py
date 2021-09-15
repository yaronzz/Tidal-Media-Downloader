#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  taskItemModel.py
@Date    :  2021/9/14
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import _thread

import aigpy.stringHelper
from tidal_dl import Type
from tidal_dl.model import Album, Track, Video, Playlist

from tidal_gui.tidalImp import tidalImp
from tidal_gui.view.taskItemView import TaskItemView
from tidal_gui.viewModel.viewModel import ViewModel


class TaskItemModel(ViewModel):
    def __init__(self, stype: Type, data):
        super(TaskItemModel, self).__init__()
        self.view = TaskItemView()
        if stype == Type.Album:
            self.__initAlbum__(data)
        elif stype == Type.Track:
            self.__initTrack__(data)
        elif stype == Type.Video:
            self.__initVideo__(data)
        elif stype == Type.Playlist:
            self.__initPlaylist__(data)

    def __initAlbum__(self, data: Album):
        title = data.title
        desc = f"by {data.artist.name} " \
               f"{tidalImp.getDurationString(data.duration)} " \
               f"Track-{data.numberOfTracks} " \
               f"Video-{data.numberOfVideos}"
        self.view.setLabel(title, desc)

        def __thread_func__(model: TaskItemModel, album: Album):
            cover = tidalImp.getCoverData(album.cover, '1280', '1280')
            self.view.setPic(cover)

            msg, tracks, videos = tidalImp.getItems(album.id, Type.Album)
            if not aigpy.stringHelper.isNull(msg):
                model.view.setErrmsg(msg)
                return
            # TODO
            for item in tracks:
                pass
            for item in videos:
                pass

        _thread.start_new_thread(__thread_func__, (self, data))

    def __initTrack__(self, data: Track):
        pass

    def __initVideo__(self, data: Video):
        pass

    def __initPlaylist__(self, data: Playlist):
        pass
