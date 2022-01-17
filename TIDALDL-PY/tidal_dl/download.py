#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   download.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import requests
import logging
import os
import datetime

import aigpy
import lyricsgenius
from tidal_dl.decryption import decrypt_file
from tidal_dl.decryption import decrypt_security_token
from tidal_dl.enums import Type, AudioQuality
from tidal_dl.model import Track, Video, Lyrics, Mix
from tidal_dl.printf import Printf
from tidal_dl.settings import Settings
from tidal_dl.tidal import TidalAPI
from tidal_dl.util import convert, downloadTrack, downloadVideo, encrypted, getVideoPath, getTrackPath, getAlbumPath, API


def __loadAPI__(user):
    API.key.accessToken = user.accessToken
    API.key.userId = user.userid
    API.key.countryCode = user.countryCode


def __downloadCover__(conf, album):
    if album == None:
        return
    path = getAlbumPath(conf, album) + '/cover.jpg'
    url = API.getCoverUrl(album.cover, "1280", "1280")
    if url is not None:
        aigpy.net.downloadFile(url, path)


def __saveAlbumInfo__(conf, album, tracks):
    if album == None:
        return
    path = getAlbumPath(conf, album) + '/AlbumInfo.txt'

    infos = ""
    infos += "[ID]          %s\n" % (str(album.id))
    infos += "[Title]       %s\n" % (str(album.title))
    infos += "[Artists]     %s\n" % (str(album.artist.name))
    infos += "[ReleaseDate] %s\n" % (str(album.releaseDate))
    infos += "[SongNum]     %s\n" % (str(album.numberOfTracks))
    infos += "[Duration]    %s\n" % (str(album.duration))
    infos += '\n'

    i = 0
    while True:
        if i >= int(album.numberOfVolumes):
            break
        i = i + 1
        infos += "===========CD %d=============\n" % i
        for item in tracks:
            if item.volumeNumber != i:
                continue
            infos += '{:<8}'.format("[%d]" % item.trackNumber)
            infos += "%s\n" % item.title
    aigpy.file.write(path, infos, "w+")


def __album__(conf, obj):
    Printf.album(obj)
    msg, tracks, videos = API.getItems(obj.id, Type.Album)
    if not aigpy.string.isNull(msg):
        Printf.err(msg)
        return
    if conf.saveAlbumInfo:
        __saveAlbumInfo__(conf, obj, tracks)
    if conf.saveCovers:
        __downloadCover__(conf, obj)
    for item in tracks:
        downloadTrack(item, obj)
    for item in videos:
        downloadVideo(item, obj)


def __track__(conf, obj):
    msg, album = API.getAlbum(obj.album.id)
    if conf.saveCovers:
        __downloadCover__(conf, album)
    downloadTrack(obj, album)


def __video__(conf, obj):
    # Printf.video(obj)
    downloadVideo(obj, obj.album)


def __artist__(conf, obj):
    msg, albums = API.getArtistAlbums(obj.id, conf.includeEP)
    Printf.artist(obj, len(albums))
    if not aigpy.string.isNull(msg):
        Printf.err(msg)
        return
    for item in albums:
        __album__(conf, item)


def __playlist__(conf, obj):
    Printf.playlist(obj)
    msg, tracks, videos = API.getItems(obj.uuid, Type.Playlist)
    if not aigpy.string.isNull(msg):
        Printf.err(msg)
        return

    for index, item in enumerate(tracks):
        mag, album = API.getAlbum(item.album.id)
        item.trackNumberOnPlaylist = index + 1
        downloadTrack(item, album, obj)
        if conf.saveCovers and not conf.usePlaylistFolder:
            __downloadCover__(conf, album)
    for item in videos:
        downloadVideo(item, None)
        

def __mix__(conf, obj: Mix):
    Printf.mix(obj)
    for index, item in enumerate(obj.tracks):
        mag, album = API.getAlbum(item.album.id)
        item.trackNumberOnPlaylist = index + 1
        downloadTrack(item, album)
        if conf.saveCovers and not conf.usePlaylistFolder:
            __downloadCover__(conf, album)
    for item in obj.videos:
        downloadVideo(item, None)


def file(user, conf, string):
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
        start(user, conf, item)


def start(user, conf, string):
    __loadAPI__(user)
    if aigpy.string.isNull(string):
        Printf.err('Please enter something.')
        return

    strings = string.split(" ")
    for item in strings:
        if aigpy.string.isNull(item):
            continue
        if os.path.exists(item):
            file(user, conf, item)
            return

        msg, etype, obj = API.getByString(item)
        if etype == Type.Null or not aigpy.string.isNull(msg):
            Printf.err(msg + " [" + item + "]")
            return

        if etype == Type.Album:
            __album__(conf, obj)
        if etype == Type.Track:
            __track__(conf, obj)
        if etype == Type.Video:
            __video__(conf, obj)
        if etype == Type.Artist:
            __artist__(conf, obj)
        if etype == Type.Playlist:
            __playlist__(conf, obj)
        if etype == Type.Mix:
            __mix__(conf, obj)
