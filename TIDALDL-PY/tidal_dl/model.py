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
    def __init__(self) -> None:
        super().__init__()
        self.trackid = None
        self.url = None
        self.urls = None
        self.codec = None
        self.encryptionKey = None
        self.soundQuality = None


class VideoStreamUrl(aigpy.model.ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.codec = None
        self.resolution = None
        self.resolutions = None
        self.m3u8Url = None


class Artist(aigpy.model.ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.name = None
        self.type = None
        self.picture = None


class Album(aigpy.model.ModelBase):
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


class Playlist(aigpy.model.ModelBase):
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


class Track(aigpy.model.ModelBase):
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


class Video(aigpy.model.ModelBase):
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


class Mix(aigpy.model.ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.id = None
        self.tracks = Track()
        self.videos = Video()


class Lyrics(aigpy.model.ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.trackId = None
        self.lyricsProvider = None
        self.providerCommontrackId = None
        self.providerLyricsId = None
        self.lyrics = None
        self.subtitles = None


class SearchDataBase(aigpy.model.ModelBase):
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


class SearchResult(aigpy.model.ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.artists = SearchArtists()
        self.albums = SearchAlbums()
        self.tracks = SearchTracks()
        self.videos = SearchVideos()
        self.playlists = SearchPlaylists()


class LoginKey(aigpy.model.ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.deviceCode = None
        self.userCode = None
        self.verificationUrl = None
        self.authCheckTimeout = None
        self.authCheckInterval = None
        self.userId = None
        self.countryCode = None
        self.accessToken = None
        self.refreshToken = None
        self.expiresIn = None
        self.pkceState = None
        self.pkceCodeVerifier = None
        self.pkceRedirectUri = None


class StreamRespond(aigpy.model.ModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.trackid = None
        self.videoid = None
        self.streamType = None
        self.assetPresentation = None
        self.audioMode = None
        self.audioQuality = None
        self.videoQuality = None
        self.manifestMimeType = None
        self.manifest = None
