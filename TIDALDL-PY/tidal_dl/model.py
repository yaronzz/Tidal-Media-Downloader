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
    def __init__(self) -> None:
        super().__init__()
        self.trackid = None
        self.url = None
        self.codec = None
        self.encryptionKey = None
        self.soundQuality = None


class VideoStreamUrl(ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.codec = None
        self.resolution = None
        self.resolutions = None
        self.m3u8Url = None


class Artist(ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.name = None
        self.type = None
        self.picture = None


class Album(ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.title = None
        self.duration = 0
        self.numberOfTracks = 0
        self.numberOfVideos = 0
        self.numberOfVolumes = 0
        self.releaseDate = None
        self.type = None
        self.version = None
        self.cover = None
        self.explicit = False
        self.audioQuality = None
        self.audioModes = None
        self.artist = Artist()
        self.artists = Artist()


class Playlist(ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.uuid = None
        self.title = None
        self.numberOfTracks = 0
        self.numberOfVideos = 0
        self.description = None
        self.duration = 0
        self.image = None
        self.squareImage = None


class Track(ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.title = None
        self.duration = 0
        self.trackNumber = 0
        self.volumeNumber = 0
        self.trackNumberOnPlaylist = 0
        self.version = None
        self.isrc = None
        self.explicit = False
        self.audioQuality = None
        self.copyRight = None
        self.artist = Artist()
        self.artists = Artist()
        self.album = Album()
        self.allowStreaming = False
        self.playlist = None


class Video(ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.title = None
        self.duration = 0
        self.imageID = None
        self.trackNumber = 0
        self.releaseDate = None
        self.version = None
        self.quality = None
        self.explicit = False
        self.artist = Artist()
        self.artists = Artist()
        self.album = Album()
        self.allowStreaming = False
        self.playlist = None


class Mix(ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.tracks = Track()
        self.videos = Video()


class Lyrics(ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.trackId = None
        self.lyricsProvider = None
        self.providerCommontrackId = None
        self.providerLyricsId = None
        self.lyrics = None
        self.subtitles = None


class SearchDataBase(ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.limit = 0
        self.offset = 0
        self.totalNumberOfItems = 0


class SearchAlbums(SearchDataBase):
    def __init__(self) -> None:
        super().__init__()
        self.items = Album()


class SearchArtists(SearchDataBase):
    def __init__(self) -> None:
        super().__init__()
        self.items = Artist()


class SearchTracks(SearchDataBase):
    def __init__(self) -> None:
        super().__init__()
        self.items = Track()


class SearchVideos(SearchDataBase):
    def __init__(self) -> None:
        super().__init__()
        self.items = Video()


class SearchPlaylists(SearchDataBase):
    def __init__(self) -> None:
        super().__init__()
        self.items = Playlist()


class SearchResult(ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.artists = SearchArtists()
        self.albums = SearchAlbums()
        self.tracks = SearchTracks()
        self.videos = SearchVideos()
        self.playlists = SearchPlaylists()

