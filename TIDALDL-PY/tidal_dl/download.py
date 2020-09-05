#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   download.py
@Time    :   2020/08/18
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import os

import aigpy.m3u8Helper as m3u8Helper
from aigpy.tagHelper import TagTool
from aigpy.netHelper import downloadFile, downloadFileMultiThread
from aigpy.stringHelper import isNull, getSubOnlyEnd
from aigpy.pathHelper import replaceLimitChar, getFileName, remove
from aigpy.fileHelper import getFileContent

from tidal_dl.tidal import TidalAPI
from tidal_dl.enum import Type, AudioQuality, VideoQuality
from tidal_dl.printf import Printf
from tidal_dl.decryption import decrypt_security_token
from tidal_dl.decryption import decrypt_file

API = TidalAPI()

def __loadAPI__(user):
    API.key.accessToken = user.assesstoken
    API.key.userId = user.userid
    API.key.countryCode = user.countryCode
    API.key.sessionId = user.sessionid1


def __loadVideoAPI__(user):
    API.key.accessToken = user.assesstoken
    API.key.userId = user.userid
    API.key.countryCode = user.countryCode
    API.key.sessionId = user.sessionid2 if not isNull(user.sessionid2) else user.sessionid1



def __getIndexStr__(index):
    pre = "0"
    if index < 10:
        return pre+str(index)
    if index < 99:
        return str(index)
    return str(index)

def __getExtension__(url):
    if '.flac' in url:
        return '.flac'
    if '.mp4' in url:
        return '.mp4'
    return '.m4a'

def __getArtists__(array):
    ret = []
    for item in array:
        ret.append(item.name)
    return ret



def __setMetaData__(track, album, filepath):
    obj = TagTool(filepath)
    obj.album = track.album.title
    obj.title = track.title
    obj.artist = __getArtists__(track.artists)
    obj.copyright = track.copyRight
    obj.tracknumber = track.trackNumber
    obj.discnumber = track.volumeNumber
    obj.isrc = track.isrc
    obj.albumartist = __getArtists__(album.artists)
    obj.date = album.releaseDate
    obj.totaldisc = album.numberOfVolumes
    if obj.totaldisc <= 1:
        obj.totaltrack = album.numberOfTracks
    coverpath = API.getCoverUrl(album.cover, "1280", "1280")
    obj.save(coverpath)
    return

def __convertToM4a__(filepath, codec):
    if 'ac4' in codec or 'mha1' in codec:
        return filepath
    if '.mp4' not in filepath:
        return filepath
    newpath = filepath.replace('.mp4', '.m4a')
    remove(newpath)
    os.rename(filepath, newpath)
    return newpath

def __getAlbumPath__(conf, album):
    # outputdir/Album/artist/
    artist = replaceLimitChar(album.artists[0].name, '-')
    base = conf.downloadPath + '/Album/' + artist + '/'
    
    #album folder pre: [ME][ID]
    flag = API.getFlag(album, Type.Album, True, "")
    if conf.audioQuality != AudioQuality.Master:
        flag = flag.replace("M","")
    if not isNull(flag):
        flag = "[" + flag + "] "
    
    sid = "[" + str(album.id) + "] " if conf.addAlbumIDBeforeFolder else ""

    #album and addyear
    albumname = replaceLimitChar(album.title, '-')
    year = ""
    if conf.addYear:
        year = "[" + getSubOnlyEnd(album.releaseDate, '-') + "] "
    return base + flag + sid + year + albumname + '/'

def __getPlaylistPath__(conf, playlist):
    pass

def __getTrackPath__(conf, track, stream, album=None, playlist=None):
    if album is not None:
        base = __getAlbumPath__(conf, album)
    if playlist is not None:
        base = __getPlaylistPath__(conf, playlist)
    #CD
    if album.numberOfVolumes > 1:
        base += 'CD' + str(track.volumeNumber) + '/'
    # hyphen
    hyphen = ' - ' if conf.addHyphen else ' '
    # get number
    number = ''
    if conf.useTrackNumber:
        number = __getIndexStr__(track.trackNumber) + hyphen
    # get artist
    artist = ''
    if conf.artistBeforeTitle:
        artist = replaceLimitChar(track.artists[0].name, '-') + hyphen
    # get explicit
    explicit = "(Explicit)" if conf.addExplicitTag and track.explicit else ''
    # title
    title = track.title
    if not isNull(track.version):
        title += ' - ' + track.version
    title = replaceLimitChar(title, '-')
    # extension
    extension = __getExtension__(stream.url)
    return base + number + artist + title + explicit + extension


def __getVideoPath__(conf, video, album=None, playlist=None):
    if album is not None:
        base = __getAlbumPath__(conf, album)
    elif playlist is not None:
        base = __getPlaylistPath__(conf, playlist)
    else:
        base = conf.downloadPath + '/Video/'
     
    # hyphen
    hyphen = ' - ' if conf.addHyphen else ' '
    # get number
    number = ''
    if conf.useTrackNumber:
        number = __getIndexStr__(video.trackNumber) + hyphen
    # get artist
    artist = ''
    if conf.artistBeforeTitle:
        artist = replaceLimitChar(video.artists[0].name, '-') + hyphen
    # get explicit
    explicit = "(Explicit)" if conf.addExplicitTag and video.explicit else ''
    # title
    title = replaceLimitChar(video.title, '-')
    # extension
    extension = ".mp4"
    return base + number + artist + title + explicit + extension
    




def __downloadVideo__(conf, video, album=None, playlist=None):
    msg, stream = API.getVideoStreamUrl(video.id, conf.videoQuality)
    if not isNull(msg):
        Printf.err(video.title + "." + msg)
        return
    path = __getVideoPath__(conf, video, album, playlist)
    if m3u8Helper.download(stream.m3u8Url, path):
        Printf.success(getFileName(path))
    else:
        Printf.err("\nDownload failed!" + getFileName(path) )

def __downloadTrack__(conf, track, album=None, playlist=None):
    try:
        msg, stream = API.getStreamUrl(track.id, conf.audioQuality)
        if not isNull(msg) or stream is None:
            Printf.err(track.title + "." + msg)
            return
        path = __getTrackPath__(conf, track, stream, album, playlist)

        # Printf.info("Download \"" + track.title + "\" Codec: " + stream.codec)
        check, err = downloadFileMultiThread(stream.url, path + '.part', stimeout=20, showprogress=True)
        if not check:
            Printf.err("Download failed!" + getFileName(path) + ' (' + str(err) + ')')
            return
        # encrypted -> decrypt and remove encrypted file
        if isNull(stream.encryptionKey):
            os.replace(path + '.part', path)
        else:
            key, nonce = decrypt_security_token(stream.encryptionKey)
            decrypt_file(path + '.part', path, key, nonce)
            os.remove(path +'.part')

        path = __convertToM4a__(path, stream.codec)
        __setMetaData__(track, album, path)
        Printf.success(getFileName(path))
    except Exception as e:
        Printf.err("Download failed!" + track.title + ' (' + str(e) + ')')

def __downloadCover__(conf, album):
    if album == None:
        return
    path = __getAlbumPath__(conf, album) + '/cover.jpg'
    url = API.getCoverUrl(album.cover, "1280", "1280")
    downloadFile(url, path)







def __album__(conf, obj):
    Printf.album(obj)
    msg, tracks, videos = API.getItems(obj.id, Type.Album)
    if not isNull(msg):
        Printf.err(msg)
        return
    if conf.saveCovers:
        __downloadCover__(conf, obj)
    for item in tracks:
        __downloadTrack__(conf, item, obj)
    for item in videos:
        __downloadVideo__(conf, item, obj)

def __track__(conf, obj):
    Printf.track(obj)
    msg, album = API.getAlbum(obj.album.id)
    if conf.saveCovers:
        __downloadCover__(conf, album)
    __downloadTrack__(conf, obj, album)

def __video__(conf, obj):
    Printf.video(obj)
    __downloadVideo__(conf, obj, obj.album)

def __artist__(conf, obj):
    Printf.artist(obj)
    msg, albums = API.getArtistAlbums(obj.id, conf.includeEP)
    if not isNull(msg):
        Printf.err(msg)
        return
    for item in albums:
        __album__(conf, item)

def __playlist__(conf, obj):
    Printf.playlist(obj)
    msg, tracks, videos = API.getItems(obj.uuid, Type.Playlist)
    if not isNull(msg):
        Printf.err(msg)
        return

    for item in tracks:
        mag, album = API.getAlbum(item.album.id)
        __downloadTrack__(conf, item, album)
    for item in videos:
        __downloadVideo__(conf, item, None)

def __file__(user, conf, string):
    txt = getFileContent(string)
    if isNull(txt):
        Printf.err("Nothing can read!")
        return
    array = txt.split('\n')
    for item in array:
        if isNull(item):
            continue
        if item[0] == '#':
            continue
        if item[0] == '[':
            continue
        start(user, conf, item)

def start(user, conf, string):
    __loadAPI__(user)

    if os.path.exists(string):
        __file__(user, conf, string)
        return

    msg, etype, obj = API.getByString(string)
    if etype == Type.Null or not isNull(msg):
        Printf.err(msg)
        return

    if etype == Type.Album:
        __album__(conf, obj)
    if etype == Type.Track:
        __track__(conf, obj)
    if etype == Type.Video:
        __loadVideoAPI__(user)
        __video__(conf, obj)
    if etype == Type.Artist:
        __artist__(conf, obj)
    if etype == Type.Playlist:
        __playlist__(conf, obj)



