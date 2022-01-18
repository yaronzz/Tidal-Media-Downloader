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
import time
import requests

import aigpy
import lyricsgenius
import datetime
from tidal_dl import apiKey
import tidal_dl
from tidal_dl.decryption import decrypt_file
from tidal_dl.decryption import decrypt_security_token
from tidal_dl.enums import Type, AudioQuality
from tidal_dl.lang.language import initLang
from tidal_dl.model import Track, Video, Lyrics, Mix, Album
from tidal_dl.printf import Printf
from tidal_dl.settings import Settings, TokenSettings, getLogPath
from tidal_dl.tidal import TidalAPI

TOKEN = TokenSettings.read()
CONF = Settings.read()
LANG = initLang(CONF.language)
API = TidalAPI()
API.apiKey = apiKey.getItem(CONF.apiKeyIndex)

logging.basicConfig(filename=getLogPath(),
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


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
    base = conf.downloadPath + '/'
    if conf.addTypeFolder:
        base = base + 'Album/'
    artist = aigpy.path.replaceLimitChar(getArtistsName(album.artists), '-')
    albumArtistName = album.artist.name if album.artist is not None else ""
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
    retpath = retpath.replace(R"{None}", "")
    retpath = stripPath(retpath.strip())
    return base + retpath


def getPlaylistPath(conf: Settings, playlist):
    # outputdir/Playlist/
    base = conf.downloadPath + '/'
    if conf.addTypeFolder:
        base = base + 'Playlist/'
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
    artists = aigpy.path.replaceLimitChar(getArtistsName(track.artists), '-')
    artist = track.artist.name if track.artist is not None else ""
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
    retpath = retpath.replace(R"{ArtistsName}", artists.strip())
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
        base = conf.downloadPath + '/'
        if conf.addTypeFolder:
            base = base + 'Video/'

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


def encrypted(stream, srcPath, descPath):
    if aigpy.string.isNull(stream.encryptionKey):
        os.replace(srcPath, descPath)
    else:
        key, nonce = decrypt_security_token(stream.encryptionKey)
        decrypt_file(srcPath, descPath, key, nonce)
        os.remove(srcPath)


def getAudioQualityList():
    return map(lambda quality: quality.name, tidal_dl.enums.AudioQuality)

def getCurAudioQuality():
    return CONF.audioQuality.name

def setCurAudioQuality(text):
    if CONF.audioQuality.name == text:
        return
    for item in tidal_dl.enums.AudioQuality:
        if item.name == text:
            CONF.audioQuality = item
            break
    Settings.save(CONF)

def getVideoQualityList():
    return map(lambda quality: quality.name, tidal_dl.enums.VideoQuality)

def getCurVideoQuality():
    return CONF.videoQuality.name

def setCurVideoQuality(text):
    if CONF.videoQuality.name == text:
        return
    for item in tidal_dl.enums.VideoQuality:
        if item.name == text:
            CONF.videoQuality = item
            break
    Settings.save(CONF)

def skip(path, url):
    if CONF.checkExist and isNeedDownload(path, url) is False:
        return True
    return False


def convert(srcPath, stream):
    if CONF.onlyM4a:
        return convertToM4a(srcPath, stream.codec)
    return srcPath


def downloadTrack(track: Track, album=None, playlist=None, userProgress=None, partSize=1048576):
    try:
        msg, stream = API.getStreamUrl(track.id, CONF.audioQuality)
        if not aigpy.string.isNull(msg) or stream is None:
            Printf.err(track.title + "." + msg)
            return False, msg
        if CONF.showTrackInfo:
            Printf.track(track, stream)
        if userProgress is not None:
            userProgress.updateStream(stream)
        path = getTrackPath(CONF, track, stream, album, playlist)

        # check exist
        if skip(path, stream.url):
            Printf.success(aigpy.path.getFileName(path) + " (skip:already exists!)")
            return True, ""

        # download
        logging.info("[DL Track] name=" + aigpy.path.getFileName(path) + "\nurl=" + stream.url)
        tool = aigpy.download.DownloadTool(path + '.part', [stream.url])
        tool.setUserProgress(userProgress)
        tool.setPartSize(partSize)
        check, err = tool.start(CONF.showProgress)
        if not check:
            Printf.err("Download failed! " + aigpy.path.getFileName(path) + ' (' + str(err) + ')')
            return False, str(err)

        # encrypted -> decrypt and remove encrypted file
        encrypted(stream, path + '.part', path)

        # convert
        path = convert(path, stream)

        # contributors
        msg, contributors = API.getTrackContributors(track.id)
        msg, tidalLyrics = API.getLyrics(track.id)

        lyrics = '' if tidalLyrics is None else tidalLyrics.subtitles
        if CONF.lyricFile:
            if tidalLyrics is None:
                Printf.info(f'Failed to get lyrics from tidal!"{track.title}"')
            else:
                lrcPath = path.rsplit(".", 1)[0] + '.lrc'
                aigpy.fileHelper.write(lrcPath, tidalLyrics.subtitles, 'w')

        setMetaData(track, album, path, contributors, lyrics)
        Printf.success(aigpy.path.getFileName(path))
        return True, ""
    except Exception as e:
        Printf.err("Download failed! " + track.title + ' (' + str(e) + ')')
        return False, str(e)


def downloadVideo(video: Video, album=None, playlist=None):
    msg, stream = API.getVideoStreamUrl(video.id, CONF.videoQuality)
    Printf.video(video, stream)
    if not aigpy.string.isNull(msg):
        Printf.err(video.title + "." + msg)
        return False, msg
    path = getVideoPath(CONF, video, album, playlist)

    logging.info("[DL Video] name=" + aigpy.path.getFileName(path) + "\nurl=" + stream.m3u8Url)
    m3u8content = requests.get(stream.m3u8Url).content
    if m3u8content is None:
        Printf.err(video.title + ' get m3u8 content failed.')
        return False, "Get m3u8 content failed"

    urls = aigpy.m3u8.parseTsUrls(m3u8content)
    if len(urls) <= 0:
        Printf.err(video.title + ' parse ts urls failed.')
        logging.info("[DL Video] title=" + video.title + "\m3u8Content=" + str(m3u8content))
        return False, 'Parse ts urls failed.'

    check, msg = aigpy.m3u8.downloadByTsUrls(urls, path)
    # check, msg = aigpy.m3u8.download(stream.m3u8Url, path)
    if check is True:
        Printf.success(aigpy.path.getFileName(path))
        return True, ''
    else:
        Printf.err("\nDownload failed!" + msg + '(' + aigpy.path.getFileName(path) + ')')
        return False, msg


def displayTime(seconds, granularity=2):
    if seconds <= 0:
        return "unknown"

    result = []
    intervals = (
        ('weeks', 604800),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1),
    )

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def loginByConfig():
    if aigpy.stringHelper.isNull(TOKEN.accessToken):
        return False

    msg, check = API.verifyAccessToken(TOKEN.accessToken)
    if check:
        Printf.info(LANG.MSG_VALID_ACCESSTOKEN.format(displayTime(int(TOKEN.expiresAfter - time.time()))))
        API.key.countryCode = TOKEN.countryCode
        API.key.userId = TOKEN.userid
        API.key.accessToken = TOKEN.accessToken
        return True

    Printf.info(LANG.MSG_INVAILD_ACCESSTOKEN)
    msg, check = API.refreshAccessToken(TOKEN.refreshToken)
    if check:
        Printf.success(LANG.MSG_VALID_ACCESSTOKEN.format(displayTime(int(API.key.expiresIn))))
        TOKEN.userid = API.key.userId
        TOKEN.countryCode = API.key.countryCode
        TOKEN.accessToken = API.key.accessToken
        TOKEN.expiresAfter = time.time() + int(API.key.expiresIn)
        TokenSettings.save(TOKEN)
        return True
    else:
        tmp = TokenSettings()  # clears saved tokens
        TokenSettings.save(tmp)
        return False

def loginByWeb():
    start = time.time()
    elapsed = 0
    while elapsed < API.key.authCheckTimeout:
        elapsed = time.time() - start
        msg, check = API.checkAuthStatus()
        if not check:
            if msg == "pending":
                time.sleep(API.key.authCheckInterval + 1)
                continue
            return False
        if check:
            Printf.success(LANG.MSG_VALID_ACCESSTOKEN.format(displayTime(int(API.key.expiresIn))))
            TOKEN.userid = API.key.userId
            TOKEN.countryCode = API.key.countryCode
            TOKEN.accessToken = API.key.accessToken
            TOKEN.refreshToken = API.key.refreshToken
            TOKEN.expiresAfter = time.time() + int(API.key.expiresIn)
            TokenSettings.save(TOKEN)
            return True
        
    Printf.err(LANG.AUTH_TIMEOUT)
    return False

def getArtistsNames(artists):  # : list[tidal_dl.model.Artist]
    ret = []
    for item in artists:
        ret.append(item.name)
    return ','.join(ret)

def getDurationString(seconds: int):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)

def getBasePath(model):
    if isinstance(model, tidal_dl.model.Album):
        return getAlbumPath(CONF, model)
    if isinstance(model, tidal_dl.model.Playlist):
        return getPlaylistPath(CONF, model)
    if isinstance(model, tidal_dl.model.Track):
        return getAlbumPath(CONF, model.album)
    if isinstance(model, tidal_dl.model.Video):
        filePath = getVideoPath(CONF, model, model.album, model.playlist)
        return aigpy.pathHelper.getDirName(filePath)
    return './'

def getFilePath(model, stream=None):
    if isinstance(model, tidal_dl.model.Track):
        return getTrackPath(CONF, model, stream, model.album, model.playlist)
    if isinstance(model, tidal_dl.model.Video):
        return getVideoPath(CONF, model, model.album, model.playlist)
    return './'
