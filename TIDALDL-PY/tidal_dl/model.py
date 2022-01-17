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
from aigpy.modelHelper import ModelBase


class StreamUrl(ModelBase):
    trackid = None
    url = None
    codec = None
    encryptionKey = None
    soundQuality = None


class VideoStreamUrl(ModelBase):
    codec = None
    resolution = None
    resolutions = None
    m3u8Url = None


class Artist(ModelBase):
    id = None
    name = None
    type = None
    picture = None


class Album(ModelBase):
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


class Playlist(ModelBase):
    uuid = None
    title = None
    numberOfTracks = 0
    numberOfVideos = 0
    description = None
    duration = 0
    image = None
    squareImage = None


class Track(ModelBase):
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


class Video(ModelBase):
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


class Mix(ModelBase):
    id = None
    tracks = Track()
    videos = Video()


class Lyrics(ModelBase):
    trackId = None
    lyricsProvider = None
    providerCommontrackId = None
    providerLyricsId = None
    lyrics = None
    subtitles = None


class SearchDataBase(ModelBase):
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


class SearchResult(ModelBase):
    artists = SearchArtists()
    albums = SearchAlbums()
    tracks = SearchTracks()
    videos = SearchVideos()
    playlists = SearchPlaylists()
