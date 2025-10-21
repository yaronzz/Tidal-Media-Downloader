#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  paths.py
@Date    :  2022/06/10
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import os
import aigpy
import datetime

from tidal import *
from settings import *


def __fixPath__(name: str):
    return aigpy.path.replaceLimitChar(name, '-').strip()


def __getYear__(releaseDate: str):
    if releaseDate is None or releaseDate == '':
        return ''
    return aigpy.string.getSubOnlyEnd(releaseDate, '-')


def __getDurationStr__(seconds):
    time_string = str(datetime.timedelta(seconds=seconds))
    if time_string.startswith('0:'):
        time_string = time_string[2:]
    return time_string


def __getExtension__(stream: StreamUrl):
    if '.flac' in stream.url:
        return '.flac'
    if '.mp4' in stream.url:
        if 'ac4' in stream.codec or 'mha1' in stream.codec:
            return '.mp4'
        elif 'flac' in stream.codec:
            return '.flac'
        return '.m4a'
    return '.m4a'


def getAlbumPath(album):
    artistName = __fixPath__(TIDAL_API.getArtistsName(album.artists))
    albumArtistName = __fixPath__(album.artist.name) if album.artist is not None else ""

    # album folder pre: [ME]
    flag = TIDAL_API.getFlag(album, Type.Album, True, "")
    if SETTINGS.audioQuality != AudioQuality.Master and SETTINGS.audioQuality != AudioQuality.Max:
        flag = flag.replace("M", "")
    if flag != "":
        flag = "[" + flag + "] "

    # album and addyear
    albumName = __fixPath__(album.title)
    year = __getYear__(album.releaseDate)

    # avoid artist(s) and album name are too long
    if len(albumName + albumArtistName) > 120:
        albumName = albumName[:70] + "..."
        albumArtistName = albumArtistName[:50] + "..."
    else:
        if len(albumName) > 100:
            albumName = albumName[:100] + "..."
        if len(albumArtistName) > 100:
            albumArtistName = albumArtistName[:100] + "..."
    if len(artistName) > 50:
        artistName = artistName[:50] + "..." 

    # retpath
    retpath = SETTINGS.albumFolderFormat
    if retpath is None or len(retpath) <= 0:
        retpath = SETTINGS.getDefaultAlbumFolderFormat()
    retpath = retpath.replace(R"{ArtistName}", artistName)
    retpath = retpath.replace(R"{AlbumArtistName}", albumArtistName)
    retpath = retpath.replace(R"{Flag}", flag)
    retpath = retpath.replace(R"{AlbumID}", str(album.id))
    retpath = retpath.replace(R"{AlbumYear}", year)
    retpath = retpath.replace(R"{AlbumTitle}", albumName)
    retpath = retpath.replace(R"{AudioQuality}", album.audioQuality)
    retpath = retpath.replace(R"{DurationSeconds}", str(album.duration))
    retpath = retpath.replace(R"{Duration}", __getDurationStr__(album.duration))
    retpath = retpath.replace(R"{NumberOfTracks}", str(album.numberOfTracks))
    retpath = retpath.replace(R"{NumberOfVideos}", str(album.numberOfVideos))
    retpath = retpath.replace(R"{NumberOfVolumes}", str(album.numberOfVolumes))
    retpath = retpath.replace(R"{ReleaseDate}", str(album.releaseDate))
    retpath = retpath.replace(R"{RecordType}", album.type)
    retpath = retpath.replace(R"{None}", "")
    retpath = retpath.strip()
    return f"{SETTINGS.downloadPath}/{retpath}"

def getPlaylistPath(playlist):
    playlistName = __fixPath__(playlist.title)

    # retpath
    retpath = SETTINGS.playlistFolderFormat
    if retpath is None or len(retpath) <= 0:
        retpath = SETTINGS.getDefaultPlaylistFolderFormat()
    retpath = retpath.replace(R"{PlaylistUUID}", str(playlist.uuid))
    retpath = retpath.replace(R"{PlaylistName}", playlistName)
    return f"{SETTINGS.downloadPath}/{retpath}"

def getTrackPath(track, stream, album=None, playlist=None):
    base = './'
    number = str(track.trackNumber).rjust(2, '0')
    if album is not None:
        base = getAlbumPath(album)
        if album.numberOfVolumes > 1:
            base += f'/CD{str(track.volumeNumber)}'

    if playlist is not None and SETTINGS.usePlaylistFolder:
        base = getPlaylistPath(playlist)
        number = str(track.trackNumberOnPlaylist).rjust(2, '0')

    # artist
    artists = __fixPath__(TIDAL_API.getArtistsName(track.artists))
    artist = __fixPath__(track.artist.name) if track.artist is not None else ""

    # title
    title = __fixPath__(track.title)
    if not aigpy.string.isNull(track.version):
        title += f' ({__fixPath__(track.version)})'

    # explicit
    explicit = "(Explicit)" if track.explicit else ''

    # album and addyear
    albumName = __fixPath__(album.title) if album is not None else ''
    year = __getYear__(album.releaseDate) if album is not None else ''

    # extension
    extension = __getExtension__(stream)
    
    # avoid artist(s) and album name are too long
    if len(artist + albumName) > 100:
        artist = artist[:50] + "..."
        albumName = albumName[:50] + "..."
    else:
        if len(artists) > 100:
            artists = artists[:100] + "..."
        if len(albumName) > 100:
            albumName = albumName[:100] + "..."
    if len(artist) > 50:
        artist = artist[:50] + "..."

    retpath = SETTINGS.trackFileFormat
    if retpath is None or len(retpath) <= 0:
        retpath = SETTINGS.getDefaultTrackFileFormat()
    retpath = retpath.replace(R"{TrackNumber}", number)
    retpath = retpath.replace(R"{ArtistName}", artist)
    retpath = retpath.replace(R"{ArtistsName}", artists)
    retpath = retpath.replace(R"{TrackTitle}", title)
    retpath = retpath.replace(R"{ExplicitFlag}", explicit)
    retpath = retpath.replace(R"{AlbumYear}", year)
    retpath = retpath.replace(R"{AlbumTitle}", albumName)
    retpath = retpath.replace(R"{AudioQuality}", track.audioQuality)
    retpath = retpath.replace(R"{DurationSeconds}", str(track.duration))
    retpath = retpath.replace(R"{Duration}", __getDurationStr__(track.duration))
    retpath = retpath.replace(R"{TrackID}", str(track.id))
    retpath = retpath.strip()

    # avoid file path too long
    fullpath = f"{base}/{retpath}"
    fullpath = os.path.abspath(fullpath)
    if len(fullpath) > 240:
        fullpath = fullpath[:240]

    return f"{fullpath}{extension}"


def getVideoPath(video, album=None, playlist=None):
    base = SETTINGS.downloadPath + '/Video/'
    if album is not None and album.title is not None:
        base = getAlbumPath(album)
    elif playlist is not None:
        base = getPlaylistPath(playlist)

    # get number
    number = str(video.trackNumber).rjust(2, '0')

    # get artist
    artists = __fixPath__(TIDAL_API.getArtistsName(video.artists))
    artist = __fixPath__(video.artist.name) if video.artist is not None else ""

    # explicit
    explicit = "(Explicit)" if video.explicit else ''

    # title and year and extension
    title = __fixPath__(video.title)
    year = __getYear__(video.releaseDate)
    extension = ".mp4"

    retpath = SETTINGS.videoFileFormat
    if retpath is None or len(retpath) <= 0:
        retpath = SETTINGS.getDefaultVideoFileFormat()
    retpath = retpath.replace(R"{VideoNumber}", number)
    retpath = retpath.replace(R"{ArtistName}", artist)
    retpath = retpath.replace(R"{ArtistsName}", artists)
    retpath = retpath.replace(R"{VideoTitle}", title)
    retpath = retpath.replace(R"{ExplicitFlag}", explicit)
    retpath = retpath.replace(R"{VideoYear}", year)
    retpath = retpath.replace(R"{VideoID}", str(video.id))
    retpath = retpath.strip()
    return f"{base}/{retpath}{extension}"


def __getHomePath__():
    if "XDG_CONFIG_HOME" in os.environ:
        return os.environ['XDG_CONFIG_HOME']
    elif "HOME" in os.environ:
        return os.environ['HOME']
    elif "HOMEDRIVE" in os.environ and "HOMEPATH" in os.environ:
        return os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    else:
        return os.path.abspath("./")

def getLogPath():
    return __getHomePath__() + '/.tidal-dl.log'

def getTokenPath():
    return __getHomePath__() + '/.tidal-dl.token.json'

def getProfilePath():
    return __getHomePath__() + '/.tidal-dl.json'
