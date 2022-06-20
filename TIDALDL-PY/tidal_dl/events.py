#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  events.py
@Date    :  2022/06/10
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""

import aigpy
import time

from tidal_dl.model import *
from tidal_dl.enums import *
from tidal_dl.tidal import *
from tidal_dl.printf import *
from tidal_dl.download import *

'''
=================================
START DOWNLOAD
=================================
'''


def __album__(obj: Album):
    try:
        Printf.album(obj)
        tracks, videos = TIDAL_API.getItems(obj.id, Type.Album)
        if SETTINGS.saveAlbumInfo:
            downloadAlbumInfo(obj, tracks)
        if SETTINGS.saveCovers:
            downloadCover(obj)
        for item in tracks:
            downloadTrack(item, obj)
        for item in videos:
            downloadVideo(item, obj)
    except Exception as e:
        Printf.err(str(e))


def __track__(obj: Track):
    try:
        album = TIDAL_API.getAlbum(obj.album.id)
        if SETTINGS.saveCovers:
            downloadCover(album)
        downloadTrack(obj, album)
    except Exception as e:
        Printf.err(str(e))


def __video__(obj: Video):
    try:
        # Printf.video(obj)
        downloadVideo(obj, obj.album)
    except Exception as e:
        Printf.err(str(e))


def __artist__(obj: Artist):
    try:
        albums = TIDAL_API.getArtistAlbums(obj.id, SETTINGS.includeEP)
        Printf.artist(obj, len(albums))
        for item in albums:
            __album__(item)
    except Exception as e:
        Printf.err(str(e))


def __playlist__(obj: Playlist):
    try:
        Printf.playlist(obj)
        tracks, videos = TIDAL_API.getItems(obj.uuid, Type.Playlist)

        for index, item in enumerate(tracks):
            album = TIDAL_API.getAlbum(item.album.id)
            item.trackNumberOnPlaylist = index + 1
            downloadTrack(item, album, obj)
            if SETTINGS.saveCovers and not SETTINGS.usePlaylistFolder:
                downloadCover(album)
        for item in videos:
            downloadVideo(item, None)
    except Exception as e:
        Printf.err(str(e))


def __mix__(obj: Mix):
    try:
        Printf.mix(obj)
        for index, item in enumerate(obj.tracks):
            album = TIDAL_API.getAlbum(item.album.id)
            item.trackNumberOnPlaylist = index + 1
            downloadTrack(item, album)
            if SETTINGS.saveCovers and not SETTINGS.usePlaylistFolder:
                downloadCover(album)

        for item in obj.videos:
            downloadVideo(item, None)
    except Exception as e:
        Printf.err(str(e))


def __dealFile__(string):
    txt = aigpy.file.getContent(string)
    if aigpy.string.isNull(txt):
        Printf.err("Nothing can read!")
        return
    array = txt.split('\n')
    for item in array:
        if aigpy.string.isNull(item):
            continue
        if item[0] == '#':
            continue
        if item[0] == '[':
            continue
        start(item)


def start(string):
    if aigpy.string.isNull(string):
        Printf.err('Please enter something.')
        return

    strings = string.split(" ")
    for item in strings:
        if aigpy.string.isNull(item):
            continue
        if os.path.exists(item):
            __dealFile__(item)
            return

        try:
            etype, obj = TIDAL_API.getByString(item)
        except Exception as e:
            Printf.err(str(e) + " [" + item + "]")
            return

        if etype == Type.Album:
            __album__(obj)
        elif etype == Type.Track:
            __track__(obj)
        elif etype == Type.Video:
            __video__(obj)
        elif etype == Type.Artist:
            __artist__(obj)
        elif etype == Type.Playlist:
            __playlist__(obj)
        elif etype == Type.Mix:
            __mix__(obj)


'''
=================================
CHANGE SETTINGS
=================================
'''


def changePathSettings():
    Printf.settings(SETTINGS)
    SETTINGS.downloadPath = Printf.enterPath(
        LANG.CHANGE_DOWNLOAD_PATH,
        LANG.MSG_PATH_ERR,
        '0',
        SETTINGS.downloadPath)
    SETTINGS.albumFolderFormat = Printf.enterFormat(
        LANG.CHANGE_ALBUM_FOLDER_FORMAT,
        SETTINGS.albumFolderFormat,
        SETTINGS.getDefaultAlbumFolderFormat())
    SETTINGS.trackFileFormat = Printf.enterFormat(
        LANG.CHANGE_TRACK_FILE_FORMAT,
        SETTINGS.trackFileFormat,
        SETTINGS.getDefaultTrackFileFormat())
    SETTINGS.videoFileFormat = Printf.enterFormat(
        LANG.CHANGE_VIDEO_FILE_FORMAT,
        SETTINGS.videoFileFormat,
        SETTINGS.getDefaultVideoFileFormat())
    SETTINGS.save()


def changeQualitySettings():
    Printf.settings(SETTINGS)
    SETTINGS.audioQuality = AudioQuality(
        int(Printf.enterLimit(LANG.CHANGE_AUDIO_QUALITY,
                              LANG.MSG_INPUT_ERR,
                              ['0', '1', '2', '3'])))
    SETTINGS.videoQuality = VideoQuality(
        int(Printf.enterLimit(LANG.CHANGE_VIDEO_QUALITY,
                              LANG.MSG_INPUT_ERR,
                              ['1080', '720', '480', '360'])))
    SETTINGS.save()


def changeSettings():
    Printf.settings(SETTINGS)
    SETTINGS.showProgress = Printf.enterBool(LANG.CHANGE_SHOW_PROGRESS)
    SETTINGS.showTrackInfo = Printf.enterBool(LANG.CHANGE_SHOW_TRACKINFO)
    SETTINGS.onlyM4a = Printf.enterBool(LANG.CHANGE_ONLYM4A)
    SETTINGS.checkExist = Printf.enterBool(LANG.CHANGE_CHECK_EXIST)
    SETTINGS.includeEP = Printf.enterBool(LANG.CHANGE_INCLUDE_EP)
    SETTINGS.saveCovers = Printf.enterBool(LANG.CHANGE_SAVE_COVERS)
    SETTINGS.saveAlbumInfo = Printf.enterBool(LANG.CHANGE_SAVE_ALBUM_INFO)
    SETTINGS.lyricFile = Printf.enterBool(LANG.CHANGE_ADD_LRC_FILE)
    SETTINGS.usePlaylistFolder = Printf.enterBool(LANG.SETTING_USE_PLAYLIST_FOLDER + "('0'-No,'1'-Yes):")
    SETTINGS.language = Printf.enter(LANG.CHANGE_LANGUAGE + "(" + getLangChoicePrint() + "):")
    LANG = setLang(SETTINGS.language)
    SETTINGS.save()


def changeApiKey():
    item = apiKey.getItem(SETTINGS.apiKeyIndex)
    ver = apiKey.getVersion()

    Printf.info(f'Current APIKeys: {str(SETTINGS.apiKeyIndex)} {item["platform"]}-{item["formats"]}')
    Printf.info(f'Current Version: {str(ver)}')
    Printf.apikeys(apiKey.getItems())
    index = int(Printf.enterLimit("APIKEY index:", LANG.MSG_INPUT_ERR, apiKey.getLimitIndexs()))

    if index != SETTINGS.apiKeyIndex:
        SETTINGS.apiKeyIndex = index
        SETTINGS.save()
        TIDAL_API.apiKey = apiKey.getItem(index)
        return True
    return False


'''
=================================
LOGIN
=================================
'''


def __displayTime__(seconds, granularity=2):
    if seconds <= 0:
        return "unknown"

    result = []
    intervals = (
        ('weeks', 604800),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1),
    )

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def loginByWeb():
    try:
        print(LANG.AUTH_START_LOGIN)
        # get device code
        url = TIDAL_API.getDeviceCode()

        print(LANG.AUTH_NEXT_STEP.format(
            aigpy.cmd.green(url),
            aigpy.cmd.yellow(__displayTime__(TIDAL_API.key.authCheckTimeout))))
        print(LANG.AUTH_WAITING)

        start = time.time()
        elapsed = 0
        while elapsed < TIDAL_API.key.authCheckTimeout:
            elapsed = time.time() - start
            if not TIDAL_API.checkAuthStatus():
                time.sleep(TIDAL_API.key.authCheckInterval + 1)
                continue

            Printf.success(LANG.MSG_VALID_ACCESSTOKEN.format(
                __displayTime__(int(TIDAL_API.key.expiresIn))))

            TOKEN.userid = TIDAL_API.key.userId
            TOKEN.countryCode = TIDAL_API.key.countryCode
            TOKEN.accessToken = TIDAL_API.key.accessToken
            TOKEN.refreshToken = TIDAL_API.key.refreshToken
            TOKEN.expiresAfter = time.time() + int(TIDAL_API.key.expiresIn)
            TOKEN.save()
            return True

        raise Exception(LANG.AUTH_TIMEOUT)
    except Exception as e:
        Printf.err(f"Login failed.{str(e)}")
        return False


def loginByConfig():
    try:
        if aigpy.string.isNull(TOKEN.accessToken):
            return False

        if TIDAL_API.verifyAccessToken(TOKEN.accessToken):
            Printf.info(LANG.MSG_VALID_ACCESSTOKEN.format(
                __displayTime__(int(TOKEN.expiresAfter - time.time()))))

            TIDAL_API.key.countryCode = TOKEN.countryCode
            TIDAL_API.key.userId = TOKEN.userid
            TIDAL_API.key.accessToken = TOKEN.accessToken
            return True

        Printf.info(LANG.MSG_INVALID_ACCESSTOKEN)
        if TIDAL_API.refreshAccessToken(TOKEN.refreshToken):
            Printf.success(LANG.MSG_VALID_ACCESSTOKEN.format(
                __displayTime__(int(TIDAL_API.key.expiresIn))))

            TOKEN.userid = TIDAL_API.key.userId
            TOKEN.countryCode = TIDAL_API.key.countryCode
            TOKEN.accessToken = TIDAL_API.key.accessToken
            TOKEN.expiresAfter = time.time() + int(TIDAL_API.key.expiresIn)
            TOKEN.save()
            return True
        else:
            TokenSettings().save()
            return False
    except Exception as e:
        return False


def loginByAccessToken():
    try:
        print("-------------AccessToken---------------")
        token = Printf.enter("accessToken('0' go back):")
        if token == '0':
            return
        TIDAL_API.loginByAccessToken(token, TOKEN.userid)
    except Exception as e:
        Printf.err(str(e))
        return

    print("-------------RefreshToken---------------")
    refreshToken = Printf.enter("refreshToken('0' to skip):")
    if refreshToken == '0':
        refreshToken = TOKEN.refreshToken

    TOKEN.accessToken = token
    TOKEN.refreshToken = refreshToken
    TOKEN.expiresAfter = 0
    TOKEN.countryCode = TIDAL_API.key.countryCode
    TOKEN.save()
