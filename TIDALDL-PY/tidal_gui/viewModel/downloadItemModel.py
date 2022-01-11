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

import _thread
import os
import time
from enum import Enum
import aigpy.stringHelper
from tidal_dl import Type
from tidal_dl.model import Album, Track, Video, Playlist

from tidal_gui.tidalImp import tidalImp
from tidal_gui.view.downloadItemView import DownloadItemView
from tidal_gui.viewModel.viewModel import ViewModel

class DownloadStatus(Enum):
    Wait = 0,
    Running = 1,
    Finish = 2,
    Error = 3,
    Cancel = 4,
    
_endStatus_ = [DownloadStatus.Finish, DownloadStatus.Error, DownloadStatus.Cancel]

class DownloadItemModel(ViewModel):
    def __init__(self, index, data, basePath):
        super(DownloadItemModel, self).__init__()
        self.view = DownloadItemView()
        self.data = data
        self.basePath = basePath
        self.isTrack = isinstance(data, Track)
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
    
    def __initTrack__(self, index):
        title = self.data.title
        own = self.data.album.title
        self.view.setLabel(index, title, own)

    def __initVideo__(self, index):
        title = self.data.title
        own = tidalImp.getArtistsNames(self.data.artists)
        self.view.setLabel(index, title, own)

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
            if not self.__dlTrack__():
                return
        else:
            if not self.__dlVideo__():
                return
            
        self.view.setProgress(100)
        self.__setStatus__(DownloadStatus.Finish)
    
    def __dlTrack__(self):
        try:
            track = self.data
            conf = tidalImp.getConfig()
            
            msg, stream = tidalImp.getStreamUrl(track.id, conf.audioQuality)
            if not aigpy.string.isNull(msg) or stream is None:
                self.__setStatus__(DownloadStatus.Error)
                return False
            
            tidalImp.getBasePath(track)
            path = tidalImp.getTackPath(self.basePath, track, stream) 

            # # check exist
            # if conf.checkExist and tidalImp.__isNeedDownload__(path, stream.url) == False:
            #     return True
            
            tool = aigpy.download.DownloadTool(path + '.part', [stream.url])
            check, err = tool.start(conf.showProgress)

            if not check:
                Printf.err("Download failed! " + aigpy.path.getFileName(path) + ' (' + str(err) + ')')
                return
            # encrypted -> decrypt and remove encrypted file
            if aigpy.string.isNull(stream.encryptionKey):
                os.replace(path + '.part', path)
            else:
                key, nonce = decrypt_security_token(stream.encryptionKey)
                decrypt_file(path + '.part', path, key, nonce)
                os.remove(path + '.part')

            path = __convertToM4a__(path, stream.codec)

            # contributors
            msg, contributors = API.getTrackContributors(track.id)
            msg, tidalLyrics = API.getLyrics(track.id)

            lyrics = '' if tidalLyrics is None else tidalLyrics.subtitles
            if conf.addLyrics and lyrics == '':
                lyrics = __getLyrics__(track.title, __getArtistsString__(track.artists), conf.lyricsServerProxy)

            if conf.lyricFile:
                if tidalLyrics is None:
                    Printf.info(f'Failed to get lyrics from tidal!"{track.title}"')
                else:
                    lrcPath = path.rsplit(".", 1)[0] + '.lrc'
                    aigpy.fileHelper.write(lrcPath, tidalLyrics.subtitles, 'w')

            __setMetaData__(track, album, path, contributors, lyrics)
            Printf.success(aigpy.path.getFileName(path))
        except Exception as e:
            Printf.err("Download failed! " + track.title + ' (' + str(e) + ')')
    
    def __dlVideo__(self):
        pass
