#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  util.py
@Date    :  2021/10/09
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
"""

import logging
import os

import aigpy
import lyricsgenius
import datetime
from tidal_dl.decryption import decrypt_file
from tidal_dl.decryption import decrypt_security_token
from tidal_dl.enums import Type, AudioQuality
from tidal_dl.model import Track, Video, Lyrics, Mix, Album
from tidal_dl.printf import Printf
from tidal_dl.settings import Settings
from tidal_dl.tidal import TidalAPI

API = TidalAPI()


def __getIndexStr__(index):
    pre = "0"
    if index < 10:
        return pre + str(index)
    if index < 99:
        return str(index)
    return str(index)


def __getExtension__(url):
    if '.flac' in url:
        return '.flac'
    if '.mp4' in url:
        return '.mp4'
    return '.m4a'


def __secondsToTimeStr__(seconds):
    time_string = str(datetime.timedelta(seconds=seconds))
    if time_string.startswith('0:'):
        time_string = time_string[2:]
    return time_string

def __parseContributors__(roleType, Contributors):
    if Contributors is None:
        return None
    try:
        ret = []
        for item in Contributors['items']:
            if item['role'] == roleType:
                ret.append(item['name'])
        return ret
    except:
        return None


GEMIUS = lyricsgenius.Genius('vNKbAWAE3rVY_48nRaiOrDcWNLvsxS-Z8qyG5XfEzTOtZvkTfg6P3pxOVlA2BjaW')


def getLyricsFromGemius(trackName, artistName, proxy):
    try:
        if not aigpy.string.isNull(proxy):
            GEMIUS._session.proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}',
            }

        song = GEMIUS.search_song(trackName, artistName)
        return song.lyrics
    except:
        return ""


def stripPathParts(stripped_path, separator):
    result = ""
    stripped_path = stripped_path.split(separator)
    for stripped_path_part in stripped_path:
        result += stripped_path_part.strip()
        if not stripped_path.index(stripped_path_part) == len(stripped_path) - 1:
            result += separator
    return result.strip()


def stripPath(path):
    result = stripPathParts(path, "/")
    result = stripPathParts(result, "\\")
    return result.strip()


def getArtistsName(artists):
    return ", ".join(map(lambda artist: artist.name, artists))


# "{ArtistName}/{Flag} [{AlbumID}] [{AlbumYear}] {AlbumTitle}"
def getAlbumPath(conf: Settings, album):
    base = conf.downloadPath + '/Album/'
    artist = aigpy.path.replaceLimitChar(getArtistsName(album.artists), '-')
    albumArtistName = album.artist.name if album.artist is not None else "None"
    # album folder pre: [ME][ID]
    flag = API.getFlag(album, Type.Album, True, "")
    if conf.audioQuality != AudioQuality.Master:
        flag = flag.replace("M", "")
    if not conf.addExplicitTag:
        flag = flag.replace("E", "")
    if not aigpy.string.isNull(flag):
        flag = "[" + flag + "] "

    sid = str(album.id)
    # album and addyear
    albumname = aigpy.path.replaceLimitChar(album.title, '-')
    year = ""
    if album.releaseDate is not None:
        year = aigpy.string.getSubOnlyEnd(album.releaseDate, '-')
    # retpath
    retpath = conf.albumFolderFormat
    if retpath is None or len(retpath) <= 0:
        retpath = Settings.getDefaultAlbumFolderFormat()
    retpath = retpath.replace(R"{ArtistName}", artist.strip())
    retpath = retpath.replace(R"{AlbumArtistName}", albumArtistName.strip())
    retpath = retpath.replace(R"{Flag}", flag)
    retpath = retpath.replace(R"{AlbumID}", sid)
    retpath = retpath.replace(R"{AlbumYear}", year)
    retpath = retpath.replace(R"{AlbumTitle}", albumname.strip())
    retpath = retpath.replace(R"{AudioQuality}", album.audioQuality)
    retpath = retpath.replace(R"{DurationSeconds}", str(album.duration))
    retpath = retpath.replace(R"{Duration}", __secondsToTimeStr__(album.duration))
    retpath = retpath.replace(R"{NumberOfTracks}", str(album.numberOfTracks))
    retpath = retpath.replace(R"{NumberOfVideos}", str(album.numberOfVideos))
    retpath = retpath.replace(R"{NumberOfVolumes}", str(album.numberOfVolumes))
    retpath = retpath.replace(R"{ReleaseDate}", album.releaseDate)
    retpath = retpath.replace(R"{RecordType}", album.type)
    retpath = stripPath(retpath.strip())
    return base + retpath


def getPlaylistPath(conf: Settings, playlist):
    # outputdir/Playlist/
    base = conf.downloadPath + '/Playlist/'
    # name
    name = aigpy.path.replaceLimitChar(playlist.title, '-')
    return base + name + '/'


def getTrackPath(conf: Settings, track, stream, album=None, playlist=None):
    base = './'
    if album is not None:
        base = getAlbumPath(conf, album) + '/'
        if album.numberOfVolumes > 1:
            base += 'CD' + str(track.volumeNumber) + '/'
    if playlist is not None and conf.usePlaylistFolder:
        base = getPlaylistPath(conf, playlist)
    # number
    number = __getIndexStr__(track.trackNumber)
    if playlist is not None and conf.usePlaylistFolder:
        number = __getIndexStr__(track.trackNumberOnPlaylist)
    # artist
    artist = aigpy.path.replaceLimitChar(getArtistsName(track.artists), '-')
    # title
    title = track.title
    if not aigpy.string.isNull(track.version):
        title += ' (' + track.version + ')'
    title = aigpy.path.replaceLimitChar(title, '-')
    # get explicit
    explicit = "(Explicit)" if conf.addExplicitTag and track.explicit else ''
    # album and addyear
    albumname = aigpy.path.replaceLimitChar(album.title, '-')
    year = ""
    if album.releaseDate is not None:
        year = aigpy.string.getSubOnlyEnd(album.releaseDate, '-')
    # extension
    extension = __getExtension__(stream.url)
    retpath = conf.trackFileFormat
    if retpath is None or len(retpath) <= 0:
        retpath = Settings.getDefaultTrackFileFormat()
    retpath = retpath.replace(R"{TrackNumber}", number)
    retpath = retpath.replace(R"{ArtistName}", artist.strip())
    retpath = retpath.replace(R"{TrackTitle}", title)
    retpath = retpath.replace(R"{ExplicitFlag}", explicit)
    retpath = retpath.replace(R"{AlbumYear}", year)
    retpath = retpath.replace(R"{AlbumTitle}", albumname.strip())
    retpath = retpath.replace(R"{AudioQuality}", track.audioQuality)
    retpath = retpath.replace(R"{DurationSeconds}", str(track.duration))
    retpath = retpath.replace(R"{Duration}", __secondsToTimeStr__(track.duration))
    retpath = retpath.strip()
    return base + retpath + extension


def getVideoPath(conf, video, album=None, playlist=None):
    if album is not None and album.title is not None:
        base = getAlbumPath(conf, album)
    elif playlist is not None and conf.usePlaylistFolder:
        base = getPlaylistPath(conf, playlist)
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
        artist = aigpy.path.replaceLimitChar(getArtistsName(video.artists), '-') + hyphen
    # get explicit
    explicit = "(Explicit)" if conf.addExplicitTag and video.explicit else ''
    # title
    title = aigpy.path.replaceLimitChar(video.title, '-')
    # extension
    extension = ".mp4"
    return base + number + artist.strip() + title + explicit + extension


def convertToM4a(filepath, codec):
    if 'ac4' in codec or 'mha1' in codec:
        return filepath
    if '.mp4' not in filepath:
        return filepath
    newpath = filepath.replace('.mp4', '.m4a')
    aigpy.path.remove(newpath)
    os.rename(filepath, newpath)
    return newpath


def setMetaData(track, album, filepath, contributors, lyrics):
    obj = aigpy.tag.TagTool(filepath)
    obj.album = track.album.title
    obj.title = track.title
    if not aigpy.string.isNull(track.version):
        obj.title += ' (' + track.version + ')'

    obj.artist = list(map(lambda artist: artist.name, track.artists))  # __getArtists__(track.artists)
    obj.copyright = track.copyRight
    obj.tracknumber = track.trackNumber
    obj.discnumber = track.volumeNumber
    obj.composer = __parseContributors__('Composer', contributors)
    obj.isrc = track.isrc

    obj.albumartist = list(map(lambda artist: artist.name, album.artists))  # __getArtists__(album.artists)
    obj.date = album.releaseDate
    obj.totaldisc = album.numberOfVolumes
    obj.lyrics = lyrics
    if obj.totaldisc <= 1:
        obj.totaltrack = album.numberOfTracks
    coverpath = API.getCoverUrl(album.cover, "1280", "1280")
    obj.save(coverpath)
    return


def isNeedDownload(path, url):
    curSize = aigpy.file.getSize(path)
    if curSize <= 0:
        return True
    netSize = aigpy.net.getSize(url)
    if curSize >= netSize:
        return False
    return True
