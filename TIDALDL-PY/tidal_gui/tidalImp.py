#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  tidalImp.py
@Date    :  2021/9/2
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import time

import requests
import tidal_dl.model
import tidal_dl.enums
from aigpy.stringHelper import isNull
from tidal_dl import TokenSettings, TOKEN, TidalAPI, CONF
from tidal_dl.util import getAlbumPath, getPlaylistPath, getTrackPath


class TidalImp(TidalAPI):
    def __init__(self):
        super(TidalImp, self).__init__()

    def loginByConfig(self):
        if isNull(TOKEN.accessToken):
            return False

        msg, check = self.verifyAccessToken(TOKEN.accessToken)
        if check:
            self.key.countryCode = TOKEN.countryCode
            self.key.userId = TOKEN.userid
            self.key.accessToken = TOKEN.accessToken
            return True

        msg, check = self.refreshAccessToken(TOKEN.refreshToken)
        if check:
            TOKEN.userid = self.key.userId
            TOKEN.countryCode = self.key.countryCode
            TOKEN.accessToken = self.key.accessToken
            TOKEN.expiresAfter = time.time() + int(self.key.expiresIn)
            TokenSettings.save(TOKEN)
            return True
        else:
            tmp = TokenSettings()  # clears saved tokens
            TokenSettings.save(tmp)
            return False

    def loginByWeb(self):
        start = time.time()
        elapsed = 0
        while elapsed < self.key.authCheckTimeout:
            elapsed = time.time() - start
            msg, check = self.checkAuthStatus()
            if not check:
                if msg == "pending":
                    time.sleep(self.key.authCheckInterval + 1)
                    continue
                return False
            if check:
                TOKEN.userid = self.key.userId
                TOKEN.countryCode = self.key.countryCode
                TOKEN.accessToken = self.key.accessToken
                TOKEN.refreshToken = self.key.refreshToken
                TOKEN.expiresAfter = time.time() + int(self.key.expiresIn)
                TokenSettings.save(TOKEN)
                return True
        return False

    @staticmethod
    def getArtistsNames(artists):  # : list[tidal_dl.model.Artist]
        ret = []
        for item in artists:
            ret.append(item.name)
        return ','.join(ret)

    @staticmethod
    def getDurationString(seconds: int):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def getCoverData(self, sid, width="320", height="320"):
        url = self.getCoverUrl(sid, width, height)
        try:
            respond = requests.get(url)
            return respond.content
        except:
            return ''
    
    @staticmethod 
    def getAudioQualityList():
        return map(lambda quality: quality.name, tidal_dl.enums.AudioQuality)
    
    @staticmethod
    def getVideoQualityList():
        return map(lambda quality: quality.name, tidal_dl.enums.VideoQuality)
    
    def getBasePath(self, model):
        if isinstance(model, tidal_dl.model.Album):
            return getAlbumPath(CONF, model)
        if isinstance(model, tidal_dl.model.Playlist):
            return getPlaylistPath(CONF, model)
        if isinstance(model, tidal_dl.model.Track):
            return getAlbumPath(CONF, model.album)
        if isinstance(model, tidal_dl.model.Video):
            return CONF.downloadPath + '/Video/'
        return './'

    def getConfig(self):
        return CONF
    
    # def getTackPath(self, basePath, track, stream, album=None, playlist=None):
    #     # number
    #     number = __getIndexStr__(track.trackNumber)
    #     if playlist is not None and CONF.usePlaylistFolder:
    #         number = __getIndexStr__(track.trackNumberOnPlaylist)
    #     # artist
    #     artist = aigpy.path.replaceLimitChar(__getArtistsString__(track.artists), '-')
    #     # title
    #     title = track.title
    #     if not aigpy.string.isNull(track.version):
    #         title += ' (' + track.version + ')'
    #     title = aigpy.path.replaceLimitChar(title, '-')
    #     # get explicit
    #     explicit = "(Explicit)" if CONF.addExplicitTag and track.explicit else ''
    #     # album and addyear
    #     albumname = aigpy.path.replaceLimitChar(album.title, '-')
    #     year = ""
    #     if album.releaseDate is not None:
    #         year = aigpy.string.getSubOnlyEnd(album.releaseDate, '-')
    #     # extension
    #     extension = __getExtension__(stream.url)
    #     retpath = CONF.trackFileFormat
    #     if retpath is None or len(retpath) <= 0:
    #         retpath = Settings.getDefaultTrackFileFormat()
    #     retpath = retpath.replace(R"{TrackNumber}", number)
    #     retpath = retpath.replace(R"{ArtistName}", artist.strip())
    #     retpath = retpath.replace(R"{TrackTitle}", title)
    #     retpath = retpath.replace(R"{ExplicitFlag}", explicit)
    #     retpath = retpath.replace(R"{AlbumYear}", year)
    #     retpath = retpath.replace(R"{AlbumTitle}", albumname.strip())
    #     retpath = retpath.strip()
    #     return basePath + retpath + extension
    
    # def getVideoPath(self, basePath, video):
    #     # hyphen
    #     hyphen = ' - ' if CONF.addHyphen else ' '
    #     # get number
    #     number = ''
    #     if CONF.useTrackNumber:
    #         number = __getIndexStr__(video.trackNumber) + hyphen
    #     # get artist
    #     artist = ''
    #     if CONF.artistBeforeTitle:
    #         artist = aigpy.path.replaceLimitChar(__getArtistsString__(video.artists), '-') + hyphen
    #     # get explicit
    #     explicit = "(Explicit)" if CONF.addExplicitTag and video.explicit else ''
    #     # title
    #     title = aigpy.path.replaceLimitChar(video.title, '-')
    #     # extension
    #     extension = ".mp4"
    #     return basePath + number + artist.strip() + title + explicit + extension
        
tidalImp = TidalImp()
