#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   model.py
@Time    :   2020/08/08
@Author  :   Yaronzz
@Version :   3.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import aigpy

class StreamUrl(aigpy.model.ModelBase):
    trackid = None
    url = None
    codec = None
    encryptionKey = None
    soundQuality = None


class VideoStreamUrl(aigpy.model.ModelBase):
    codec = None
    resolution = None
    resolutions = None
    m3u8Url = None


class Artist(aigpy.model.ModelBase):
    id = None
    name = None
    type = None
    picture = None


class Album(aigpy.model.ModelBase):
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


class Playlist(aigpy.model.ModelBase):
    uuid = None
    title = None
    numberOfTracks = 0
    numberOfVideos = 0
    description = None
    duration = 0
    image = None
    squareImage = None


class Track(aigpy.model.ModelBase):
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
    allowStreaming = False
    playlist = None


class Video(aigpy.model.ModelBase):
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
    artists = Artist()
    album = Album()
    allowStreaming = False
    playlist = None


class Mix(aigpy.model.ModelBase):
    id = None
    tracks = Track()
    videos = Video()


class Lyrics(aigpy.model.ModelBase):
    trackId = None
    lyricsProvider = None
    providerCommontrackId = None
    providerLyricsId = None
    lyrics = None
    subtitles = None


class SearchDataBase(aigpy.model.ModelBase):
    limit = 0
    offset = 0
    totalNumberOfItems = 0


class SearchAlbums(SearchDataBase):
    items = Album()


class SearchArtists(SearchDataBase):
    items = Artist()


class SearchTracks(SearchDataBase):
    items = Track()


class SearchVideos(SearchDataBase):
    items = Video()


class SearchPlaylists(SearchDataBase):
    items = Playlist()


class SearchResult(aigpy.model.ModelBase):
    artists = SearchArtists()
    albums = SearchAlbums()
    tracks = SearchTracks()
    videos = SearchVideos()
    playlists = SearchPlaylists()


class LoginKey(object):
    deviceCode = None
    userCode = None
    verificationUrl = None
    authCheckTimeout = None
    authCheckInterval = None
    userId = None
    countryCode = None
    accessToken = None
    refreshToken = None
    expiresIn = None


class StreamRespond(object):
    trackid = None
    videoid = None
    streamType = None
    assetPresentation = None
    audioMode = None
    audioQuality = None
    videoQuality = None
    manifestMimeType = None
    manifest = None
