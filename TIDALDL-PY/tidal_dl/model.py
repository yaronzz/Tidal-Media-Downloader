#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   model.py
@Time    :   2020/08/08
@Author  :   Yaronzz
@Version :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''

class StreamUrl(object):
    trackid = None
    url = None
    codec = None
    encryptionKey = None
    soundQuality = None

class VideoStreamUrl(object):
    codec = None
    resolution = None
    resolutions = None
    m3u8Url = None

class Artist(object):
    id = None
    name = None
    type = None
    picture = None

class Album(object):
    id = None
    title = None
    duration = 0
    numberOfTracks = 0
    numberOfVideos = 0
    numberOfVolumes = 0
    releaseDate = None
    type = None
    version = None
    cover = None
    explicit = False
    audioQuality = None
    audioModes = None
    artist = Artist()
    artists = Artist()

class Track(object):
    id = None
    title = None
    duration = 0
    trackNumber = 0
    volumeNumber = 0
    trackNumberOnPlaylist = 0
    version = None
    isrc = None
    explicit = False
    audioQuality = None
    copyRight = None
    artist = Artist()
    artists = Artist()
    album = Album()

class Video(object):
    id = None
    title = None
    duration = 0
    imageID = None
    trackNumber = 0
    releaseDate = None
    version = None
    quality = None
    explicit = False
    artist = Artist()
    artists =  Artist()
    album = Album()

class Playlist(object):
    uuid = None
    title = None
    numberOfTracks = 0
    numberOfVideos = 0
    description = None
    duration = 0
    image = None
    squareImage = None




