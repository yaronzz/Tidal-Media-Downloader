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
from tidal_dl.util import getVideoPath, getTrackPath, getAlbumPath, getArtistsName, convertToM4a, setMetaData, \
    isNeedDownload, API, getLyricsFromGemius


def __loadAPI__(user):
    API.key.accessToken = user.accessToken
    API.key.userId = user.userid
    API.key.countryCode = user.countryCode
    # API.key.sessionId = user.sessionid1


def __loadVideoAPI__(user):
    API.key.accessToken = user.accessToken
    API.key.userId = user.userid
    API.key.countryCode = user.countryCode
    # API.key.sessionId = user.sessionid2 if not aigpy.string.isNull(user.sessionid2) else user.sessionid1


# def __getIndexStr__(index):
#     pre = "0"
#     if index < 10:
#         return pre + str(index)
#     if index < 99:
#         return str(index)
#     return str(index)


# def __getExtension__(url):
#     if '.flac' in url:
#         return '.flac'
#     if '.mp4' in url:
#         return '.mp4'
#     return '.m4a'


# def __getArtists__(array):
#     ret = []
#     for item in array:
#         ret.append(item.name)
#     return ret


# def __getArtistsString__(artists):
#     return ", ".join(map(lambda artist: artist.name, artists))


# def __parseContributors__(roleType, Contributors):
#     if Contributors is None:
#         return None
#     try:
#         ret = []
#         for item in Contributors['items']:
#             if item['role'] == roleType:
#                 ret.append(item['name'])
#         return ret
#     except:
#         return None


# GEMIUS = lyricsgenius.Genius('vNKbAWAE3rVY_48nRaiOrDcWNLvsxS-Z8qyG5XfEzTOtZvkTfg6P3pxOVlA2BjaW')
#
#
# def __getLyrics__(trackName, artistName, proxy):
#     try:
#         if not aigpy.string.isNull(proxy):
#             GEMIUS._session.proxies = {
#                 'http': f'http://{proxy}',
#                 'https': f'http://{proxy}',
#             }
#
#         song = GEMIUS.search_song(trackName, artistName)
#         return song.lyrics
#     except:
#         return ""

#
# def __setMetaData__(track, album, filepath, contributors, lyrics):
#     obj = aigpy.tag.TagTool(filepath)
#     obj.album = track.album.title
#     obj.title = track.title
#     if not aigpy.string.isNull(track.version):
#         obj.title += ' (' + track.version + ')'
#
#     obj.artist =  map(lambda artist: artist.name, track.artists) # __getArtists__(track.artists)
#     obj.copyright = track.copyRight
#     obj.tracknumber = track.trackNumber
#     obj.discnumber = track.volumeNumber
#     obj.composer = __parseContributors__('Composer', contributors)
#     obj.isrc = track.isrc
#
#     obj.albumartist = map(lambda artist: artist.name, album.artists) #__getArtists__(album.artists)
#     obj.date = album.releaseDate
#     obj.totaldisc = album.numberOfVolumes
#     obj.lyrics = lyrics
#     if obj.totaldisc <= 1:
#         obj.totaltrack = album.numberOfTracks
#     coverpath = API.getCoverUrl(album.cover, "1280", "1280")
#     obj.save(coverpath)
#     return


# def __convertToM4a__(filepath, codec):
#     if 'ac4' in codec or 'mha1' in codec:
#         return filepath
#     if '.mp4' not in filepath:
#         return filepath
#     newpath = filepath.replace('.mp4', '.m4a')
#     aigpy.path.remove(newpath)
#     os.rename(filepath, newpath)
#     return newpath


# def __stripPathParts__(stripped_path, separator):
#     result = ""
#     stripped_path = stripped_path.split(separator)
#     for stripped_path_part in stripped_path:
#         result += stripped_path_part.strip()
#         if not stripped_path.index(stripped_path_part) == len(stripped_path) - 1:
#             result += separator
#     return result.strip()
#
#
# def __stripPath__(path):
#     result = __stripPathParts__(path, "/")
#     result = __stripPathParts__(result, "\\")
#     return result.strip()

# "{ArtistName}/{Flag} [{AlbumID}] [{AlbumYear}] {AlbumTitle}"
# def getAlbumPath(conf: Settings, album):
#     base = conf.downloadPath + '/Album/'
#     artist = aigpy.path.replaceLimitChar(__getArtistsString__(album.artists), '-')
#     # album folder pre: [ME][ID]
#     flag = API.getFlag(album, Type.Album, True, "")
#     if conf.audioQuality != AudioQuality.Master:
#         flag = flag.replace("M", "")
#     if not conf.addExplicitTag:
#         flag = flag.replace("E", "")
#     if not aigpy.string.isNull(flag):
#         flag = "[" + flag + "] "
#
#     sid = str(album.id)
#     # album and addyear
#     albumname = aigpy.path.replaceLimitChar(album.title, '-')
#     year = ""
#     if album.releaseDate is not None:
#         year = aigpy.string.getSubOnlyEnd(album.releaseDate, '-')
#     # retpath
#     retpath = conf.albumFolderFormat
#     if retpath is None or len(retpath) <= 0:
#         retpath = Settings.getDefaultAlbumFolderFormat()
#     retpath = retpath.replace(R"{ArtistName}", artist.strip())
#     retpath = retpath.replace(R"{Flag}", flag)
#     retpath = retpath.replace(R"{AlbumID}", sid)
#     retpath = retpath.replace(R"{AlbumYear}", year)
#     retpath = retpath.replace(R"{AlbumTitle}", albumname.strip())
#     retpath = __stripPath__(retpath.strip())
#     return base + retpath
#
#
# def __getAlbumPath2__(conf, album):
#     # outputdir/Album/artist/
#     artist = aigpy.path.replaceLimitChar(__getArtistsString__(album.artists), '-').strip()
#     base = conf.downloadPath + '/Album/' + artist + '/'
#
#     # album folder pre: [ME][ID]
#     flag = API.getFlag(album, Type.Album, True, "")
#     if conf.audioQuality != AudioQuality.Master:
#         flag = flag.replace("M", "")
#     if not conf.addExplicitTag:
#         flag = flag.replace("E", "")
#     if not aigpy.string.isNull(flag):
#         flag = "[" + flag + "] "
#
#     sid = "[" + str(album.id) + "] " if conf.addAlbumIDBeforeFolder else ""
#
#     # album and addyear
#     albumname = aigpy.path.replaceLimitChar(album.title, '-').strip()
#     year = ""
#     if conf.addYear and album.releaseDate is not None:
#         year = "[" + aigpy.string.getSubOnlyEnd(album.releaseDate, '-') + "] "
#     return base + flag + sid + year + albumname + '/'
#
#
# def getPlaylistPath(conf, playlist):
#     # outputdir/Playlist/
#     base = conf.downloadPath + '/Playlist/'
#     # name
#     name = aigpy.path.replaceLimitChar(playlist.title, '-')
#     return base + name + '/'
#
#
# # "{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
#
#
# def getTrackPath(conf: Settings, track, stream, album=None, playlist=None):
#     if album is not None:
#         base = getAlbumPath(conf, album) + '/'
#         if album.numberOfVolumes > 1:
#             base += 'CD' + str(track.volumeNumber) + '/'
#     if playlist is not None and conf.usePlaylistFolder:
#         base = getPlaylistPath(conf, playlist)
#     # number
#     number = __getIndexStr__(track.trackNumber)
#     if playlist is not None and conf.usePlaylistFolder:
#         number = __getIndexStr__(track.trackNumberOnPlaylist)
#     # artist
#     artist = aigpy.path.replaceLimitChar(__getArtistsString__(track.artists), '-')
#     # title
#     title = track.title
#     if not aigpy.string.isNull(track.version):
#         title += ' (' + track.version + ')'
#     title = aigpy.path.replaceLimitChar(title, '-')
#     # get explicit
#     explicit = "(Explicit)" if conf.addExplicitTag and track.explicit else ''
#     # album and addyear
#     albumname = aigpy.path.replaceLimitChar(album.title, '-')
#     year = ""
#     if album.releaseDate is not None:
#         year = aigpy.string.getSubOnlyEnd(album.releaseDate, '-')
#     # extension
#     extension = __getExtension__(stream.url)
#     retpath = conf.trackFileFormat
#     if retpath is None or len(retpath) <= 0:
#         retpath = Settings.getDefaultTrackFileFormat()
#     retpath = retpath.replace(R"{TrackNumber}", number)
#     retpath = retpath.replace(R"{ArtistName}", artist.strip())
#     retpath = retpath.replace(R"{TrackTitle}", title)
#     retpath = retpath.replace(R"{ExplicitFlag}", explicit)
#     retpath = retpath.replace(R"{AlbumYear}", year)
#     retpath = retpath.replace(R"{AlbumTitle}", albumname.strip())
#     retpath = retpath.strip()
#     return base + retpath + extension
#
#
# def __getTrackPath2__(conf, track, stream, album=None, playlist=None):
#     if album is not None:
#         base = getAlbumPath(conf, album)
#         if album.numberOfVolumes > 1:
#             base += 'CD' + str(track.volumeNumber) + '/'
#     if playlist is not None and conf.usePlaylistFolder:
#         base = getPlaylistPath(conf, playlist)
#
#     # hyphen
#     hyphen = ' - ' if conf.addHyphen else ' '
#     # get number
#     number = ''
#     if conf.useTrackNumber:
#         number = __getIndexStr__(track.trackNumber) + hyphen
#         if playlist is not None:
#             number = __getIndexStr__(track.trackNumberOnPlaylist) + hyphen
#     # get artist
#     artist = ''
#     if conf.artistBeforeTitle:
#         artist = aigpy.path.replaceLimitChar(__getArtistsString__(track.artists), '-') + hyphen
#     # get explicit
#     explicit = "(Explicit)" if conf.addExplicitTag and track.explicit else ''
#     # title
#     title = track.title
#     if not aigpy.string.isNull(track.version):
#         title += ' - ' + track.version
#     title = aigpy.path.replaceLimitChar(title, '-')
#     # extension
#     extension = __getExtension__(stream.url)
#     return base + number + artist.strip() + title + explicit + extension
#
#
# def getVideoPath(conf, video, album=None, playlist=None):
#     if album is not None and album.title is not None:
#         base = getAlbumPath(conf, album)
#     elif playlist is not None and conf.usePlaylistFolder:
#         base = getPlaylistPath(conf, playlist)
#     else:
#         base = conf.downloadPath + '/Video/'
#
#     # hyphen
#     hyphen = ' - ' if conf.addHyphen else ' '
#     # get number
#     number = ''
#     if conf.useTrackNumber:
#         number = __getIndexStr__(video.trackNumber) + hyphen
#     # get artist
#     artist = ''
#     if conf.artistBeforeTitle:
#         artist = aigpy.path.replaceLimitChar(__getArtistsString__(video.artists), '-') + hyphen
#     # get explicit
#     explicit = "(Explicit)" if conf.addExplicitTag and video.explicit else ''
#     # title
#     title = aigpy.path.replaceLimitChar(video.title, '-')
#     # extension
#     extension = ".mp4"
#     return base + number + artist.strip() + title + explicit + extension


# def __isNeedDownload__(path, url):
#     curSize = aigpy.file.getSize(path)
#     if curSize <= 0:
#         return True
#     netSize = aigpy.net.getSize(url)
#     if curSize >= netSize:
#         return False
#     return True



def __downloadVideo__(conf, video: Video, album=None, playlist=None):
    if video.allowStreaming is False:
        Printf.err("Download failed! " + video.title + ' not allow streaming.')
        return

    msg, stream = API.getVideoStreamUrl(video.id, conf.videoQuality)
    Printf.video(video, stream)
    if not aigpy.string.isNull(msg):
        Printf.err(video.title + "." + msg)
        return
    path = getVideoPath(conf, video, album, playlist)

    logging.info("[DL Video] name=" + aigpy.path.getFileName(path) + "\nurl=" + stream.m3u8Url)
    m3u8content = requests.get(stream.m3u8Url).content
    if m3u8content is None:
        Printf.err(video.title + ' get m3u8 content failed.')
        return
    
    urls = aigpy.m3u8.parseTsUrls(m3u8content)
    if len(urls) <= 0:
        Printf.err(video.title + ' parse ts urls failed.')
        logging.info("[DL Video] title=" + video.title + "\m3u8Content=" + str(m3u8content))
        return
    
    check, msg = aigpy.m3u8.downloadByTsUrls(urls, path)
    # check, msg = aigpy.m3u8.download(stream.m3u8Url, path)
    if check is True:
        Printf.success(aigpy.path.getFileName(path))
    else:
        Printf.err("\nDownload failed!" + msg + '(' + aigpy.path.getFileName(path) + ')')


def __downloadTrack__(conf: Settings, track: Track, album=None, playlist=None):
    try:
        # if track.allowStreaming is False:
        #     Printf.err("Download failed! " + track.title + ' not allow streaming.')
        #     return
        msg, stream = API.getStreamUrl(track.id, conf.audioQuality)
        if conf.showTrackInfo:
            Printf.track(track, stream)
        if not aigpy.string.isNull(msg) or stream is None:
            Printf.err(track.title + "." + msg)
            return
        
        path = getTrackPath(conf, track, stream, album, playlist)

        # check exist
        if conf.onlyM4a:
            if conf.checkExist and isNeedDownload(path.replace(".mp4", ".m4a"), stream.url) == False:                
                Printf.success(aigpy.path.getFileName(path) + " (skip:already exists!)")
                return
        else:
            if conf.checkExist and isNeedDownload(path, stream.url) == False:                
                Printf.success(aigpy.path.getFileName(path) + " (skip:already exists!)")
                return
        logging.info("[DL Track] name=" + aigpy.path.getFileName(path) + "\nurl=" + stream.url)
        tool = aigpy.download.DownloadTool(path + '.part', [stream.url])
        check, err = tool.start(conf.showProgress)

        if not check:
            Printf.err("Download failed! " + aigpy.path.getFileName(path) + ' (' + str(err) + ')')
            return
        # encrypted -> decrypt and remove encrypted file
        if aigpy.string.isNull(stream.encryptionKey):
            os.replace(path + '.part', path)
        else:
            key, nonce = decrypt_security_token(stream.encryptionKey)
            decrypt_file(path + '.part', path, key, nonce)
            os.remove(path + '.part')

        path = convertToM4a(path, stream.codec)

        # contributors
        msg, contributors = API.getTrackContributors(track.id)
        msg, tidalLyrics = API.getLyrics(track.id)

        lyrics = '' if tidalLyrics is None else tidalLyrics.subtitles
        if conf.addLyrics and lyrics == '':
            lyrics = getLyricsFromGemius(track.title, getArtistsName(track.artists), conf.lyricsServerProxy)

        if conf.lyricFile:
            if tidalLyrics is None:
                Printf.info(f'Failed to get lyrics from tidal!"{track.title}"')
            else:
                lrcPath = path.rsplit(".", 1)[0] + '.lrc'
                aigpy.fileHelper.write(lrcPath, tidalLyrics.subtitles, 'w')

        setMetaData(track, album, path, contributors, lyrics)
        Printf.success(aigpy.path.getFileName(path))
    except Exception as e:
        Printf.err("Download failed! " + track.title + ' (' + str(e) + ')')


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
    
    if conf.checkAlbumExist:
        # Check if the album folder exists and if it contains all of the tracks in the album
        albumPath = getAlbumPath(conf,obj)
        if os.path.exists(albumPath) and obj.numberOfTracks == len([n for n in os.listdir(albumPath) if os.path.isfile(os.path.join(albumPath, n)) and (n.endswith(".m4a") or n.endswith(".mp4"))]):
            Printf.success("%s (skip: Album already exists!)" % obj.title)
            return
    if conf.saveAlbumInfo:
        __saveAlbumInfo__(conf, obj, tracks)
    if conf.saveCovers:
        __downloadCover__(conf, obj)
    for item in tracks:
        __downloadTrack__(conf, item, obj)
    for item in videos:
        __downloadVideo__(conf, item, obj)


def __track__(conf, obj):
    msg, album = API.getAlbum(obj.album.id)
    if conf.saveCovers:
        __downloadCover__(conf, album)
    __downloadTrack__(conf, obj, album)


def __video__(conf, obj):
    # Printf.video(obj)
    __downloadVideo__(conf, obj, obj.album)


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
        __downloadTrack__(conf, item, album, obj)
        if conf.saveCovers and not conf.usePlaylistFolder:
            __downloadCover__(conf, album)
    for item in videos:
        __downloadVideo__(conf, item, None)
        

def __mix__(conf, obj: Mix):
    Printf.mix(obj)
    for index, item in enumerate(obj.tracks):
        mag, album = API.getAlbum(item.album.id)
        item.trackNumberOnPlaylist = index + 1
        __downloadTrack__(conf, item, album)
        if conf.saveCovers and not conf.usePlaylistFolder:
            __downloadCover__(conf, album)
    for item in obj.videos:
        __downloadVideo__(conf, item, None)


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
            __loadVideoAPI__(user)
            __video__(conf, obj)
        if etype == Type.Artist:
            __artist__(conf, obj)
        if etype == Type.Playlist:
            __playlist__(conf, obj)
        if etype == Type.Mix:
            __mix__(conf, obj)
