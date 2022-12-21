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
import aigpy
import logging

from tidal_dl.paths import *
from tidal_dl.printf import *
from tidal_dl.decryption import *
from tidal_dl.tidal import *

from concurrent.futures import ThreadPoolExecutor

def __isSkip__(finalpath, url):
    if not SETTINGS.checkExist:
        return False
    curSize = aigpy.file.getSize(finalpath)
    if curSize <= 0:
        return False
    netSize = aigpy.net.getSize(url)
    return curSize >= netSize


def __encrypted__(stream, srcPath, descPath):
    if aigpy.string.isNull(stream.encryptionKey):
        os.replace(srcPath, descPath)
    else:
        key, nonce = decrypt_security_token(stream.encryptionKey)
        decrypt_file(srcPath, descPath, key, nonce)
        os.remove(srcPath)


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


def __setMetaData__(track: Track, album: Album, filepath, contributors, lyrics):
    obj = aigpy.tag.TagTool(filepath)
    obj.album = track.album.title
    obj.title = track.title
    if not aigpy.string.isNull(track.version):
        obj.title += ' (' + track.version + ')'

    obj.artist = list(map(lambda artist: artist.name, track.artists))
    obj.copyright = track.copyRight
    obj.tracknumber = track.trackNumber
    obj.discnumber = track.volumeNumber
    obj.composer = __parseContributors__('Composer', contributors)
    obj.isrc = track.isrc

    obj.albumartist = list(map(lambda artist: artist.name, album.artists))
    obj.date = album.releaseDate
    obj.totaldisc = album.numberOfVolumes
    obj.lyrics = lyrics
    if obj.totaldisc <= 1:
        obj.totaltrack = album.numberOfTracks
    coverpath = TIDAL_API.getCoverUrl(album.cover, "1280", "1280")
    obj.save(coverpath)


def downloadCover(album):
    if album is None:
        return
    path = getAlbumPath(album) + '/cover.jpg'
    url = TIDAL_API.getCoverUrl(album.cover, "1280", "1280")
    aigpy.net.downloadFile(url, path)


def downloadAlbumInfo(album, tracks):
    if album is None:
        return

    path = getAlbumPath(album)
    aigpy.path.mkdirs(path)

    path += '/AlbumInfo.txt'
    infos = ""
    infos += "[ID]          %s\n" % (str(album.id))
    infos += "[Title]       %s\n" % (str(album.title))
    infos += "[Artists]     %s\n" % (TIDAL_API.getArtistsName(album.artists))
    infos += "[ReleaseDate] %s\n" % (str(album.releaseDate))
    infos += "[SongNum]     %s\n" % (str(album.numberOfTracks))
    infos += "[Duration]    %s\n" % (str(album.duration))
    infos += '\n'

    for index in range(0, album.numberOfVolumes):
        volumeNumber = index + 1
        infos += f"===========CD {volumeNumber}=============\n"
        for item in tracks:
            if item.volumeNumber != volumeNumber:
                continue
            infos += '{:<8}'.format("[%d]" % item.trackNumber)
            infos += "%s\n" % item.title
    aigpy.file.write(path, infos, "w+")


def downloadVideo(video: Video, album: Album = None, playlist: Playlist = None):
    try:
        stream = TIDAL_API.getVideoStreamUrl(video.id, SETTINGS.videoQuality)
        path = getVideoPath(video, album, playlist)

        if __isSkip__(path, stream.m3u8Url):
            Printf.success(aigpy.path.getFileName(path) + " (skip:already exists!)")
            return True, ''
        
        Printf.video(video, stream)
        logging.info("[DL Video] name=" + aigpy.path.getFileName(path) + "\nurl=" + stream.m3u8Url)

        # Sleep for human behaviour
        if SETTINGS.downloadDelay is not False:
            sleep_time = random.randint(500, 5000) / 1000
            print(f"Sleeping for {sleep_time} seconds, to mimic human behaviour and prevent too many requests error")
            time.sleep(sleep_time)
        m3u8content = requests.get(stream.m3u8Url).content
        if m3u8content is None:
            Printf.err(f"DL Video[{video.title}] getM3u8 failed.{str(e)}")
            return False, f"GetM3u8 failed.{str(e)}"

        urls = aigpy.m3u8.parseTsUrls(m3u8content)
        if len(urls) <= 0:
            Printf.err(f"DL Video[{video.title}] getTsUrls failed.{str(e)}")
            return False, "GetTsUrls failed.{str(e)}"

        check, msg = aigpy.m3u8.downloadByTsUrls(urls, path)
        if check:
            Printf.success(video.title)
            return True
        else:
            Printf.err(f"DL Video[{video.title}] failed.{msg}")
            return False, msg
    except Exception as e:
        Printf.err(f"DL Video[{video.title}] failed.{str(e)}")
        return False, str(e)


def downloadTrack(track: Track, album=None, playlist=None, userProgress=None, partSize=1048576):
    try:
        path = getTrackPath(track, album, playlist)
        if os.path.exists(path):
            Printf.success(aigpy.path.getFileName(path) + " (skip:already exists!)")
            return True, ''
        stream = TIDAL_API.getStreamUrl(track.id, SETTINGS.audioQuality)
        if SETTINGS.showTrackInfo and not SETTINGS.multiThread:
            Printf.track(track, stream)

        if userProgress is not None:
            userProgress.updateStream(stream)

        # check exist
        if __isSkip__(path, stream.url):
            Printf.success(aigpy.path.getFileName(path) + " (skip:already exists!)")
            return True, ''

        #Sleep for human behaviour
        if SETTINGS.downloadDelay is not False:
            sleep_time = random.randint(500, 5000) / 1000
            print(f"Sleeping for {sleep_time} seconds, to mimic human behaviour and prevent too many requests error")
            time.sleep(sleep_time)

        # download
        logging.info("[DL Track] name=" + aigpy.path.getFileName(path) + "\nurl=" + stream.url)

        tool = aigpy.download.DownloadTool(path + '.part', [stream.url])
        tool.setUserProgress(userProgress)
        tool.setPartSize(partSize)
        check, err = tool.start(SETTINGS.showProgress and not SETTINGS.multiThread)
        if not check:
            Printf.err(f"DL Track[{track.title}] failed.{str(err)}")
            return False, str(err)

        # encrypted -> decrypt and remove encrypted file
        __encrypted__(stream, path + '.part', path)

        # contributors
        try:
            contributors = TIDAL_API.getTrackContributors(track.id)
        except:
            contributors = None

        # lyrics
        try:
            lyrics = TIDAL_API.getLyrics(track.id).subtitles
            if SETTINGS.lyricFile:
                lrcPath = path.rsplit(".", 1)[0] + '.lrc'
                aigpy.file.write(lrcPath, lyrics, 'w')
        except:
            lyrics = ''

        __setMetaData__(track, album, path, contributors, lyrics)
        Printf.success(track.title)
        return True, ''
    except Exception as e:
        Printf.err(f"DL Track[{track.title}] failed.{str(e)}")
        return False, str(e)


def downloadTracks(tracks, album: Album = None, playlist : Playlist=None):
    def __getAlbum__(item: Track):
        album = TIDAL_API.getAlbum(item.album.id)
        if SETTINGS.saveCovers and not SETTINGS.usePlaylistFolder:
            downloadCover(album)
        return album
    
    if not SETTINGS.multiThread:
        for index, item in enumerate(tracks):
            itemAlbum = album
            if itemAlbum is None:
                itemAlbum = __getAlbum__(item)
                item.trackNumberOnPlaylist = index + 1

            downloadTrack(item, playlist=playlist, album=itemAlbum)

    else:
        thread_pool = ThreadPoolExecutor(max_workers=5)
        for index, item in enumerate(tracks):
            itemAlbum = album
            if itemAlbum is None:
                itemAlbum = __getAlbum__(item)
                item.trackNumberOnPlaylist = index + 1

            thread_pool.submit(downloadTrack, item, playlist=playlist, album=itemAlbum)

        thread_pool.shutdown(wait=True)


def downloadVideos(videos, album: Album, playlist=None):
    for video in videos:
        downloadVideo(video, album, playlist)
