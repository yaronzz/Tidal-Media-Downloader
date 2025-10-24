#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   printf.py
@Time    :   2020/08/16
@Author  :   Yaronzz
@Version :   3.0
@Contact :   yaronhuang@foxmail.com
@Desc    :
'''
from pickle import GLOBAL
import threading
import aigpy
import logging
import prettytable

import apiKey as apiKey

from model import *
from paths import *
from settings import *
from lang.language import *


VERSION = '2022.10.31.1'
__LOGO__ = f'''
 /$$$$$$$$ /$$       /$$           /$$               /$$ /$$
|__  $$__/|__/      | $$          | $$              | $$| $$
   | $$    /$$  /$$$$$$$  /$$$$$$ | $$          /$$$$$$$| $$
   | $$   | $$ /$$__  $$ |____  $$| $$ /$$$$$$ /$$__  $$| $$
   | $$   | $$| $$  | $$  /$$$$$$$| $$|______/| $$  | $$| $$
   | $$   | $$| $$  | $$ /$$__  $$| $$        | $$  | $$| $$
   | $$   | $$|  $$$$$$$|  $$$$$$$| $$        |  $$$$$$$| $$
   |__/   |__/ \_______/ \_______/|__/         \_______/|__/

       https://github.com/yaronzz/Tidal-Media-Downloader

                        {VERSION}
'''

print_mutex = threading.Lock()


class Printf(object):

    @staticmethod
    def _mask_listener_secret(secret):
        if not secret:
            return ""
        secret = str(secret)
        if len(secret) <= 4:
            return "*" * len(secret)
        return "*" * (len(secret) - 4) + secret[-4:]

    @staticmethod
    def logo():
        print(__LOGO__)
        logging.info(__LOGO__)

    @staticmethod
    def __gettable__(columns, rows):
        tb = prettytable.PrettyTable()
        tb.field_names = list(aigpy.cmd.green(item) for item in columns)
        tb.align = 'l'
        for item in rows:
            tb.add_row(item)
        return tb

    @staticmethod
    def usage():
        print("=============TIDAL-DL HELP==============")
        tb = Printf.__gettable__(["OPTION", "DESC"], [
            ["-h or --help",        "show help-message"],
            ["-v or --version",     "show version"],
            ["-g or --gui",         "show simple-gui"],
            ["-o or --output",      "download path"],
            ["-l or --link",        "url/id/filePath"],
            ["-q or --quality",     "track quality('Normal','High,'HiFi','Master')"],
            ["-r or --resolution",  "video resolution('P1080', 'P720', 'P480', 'P360')"],
            ["--listen",            "start HTTP listener mode"]
        ])
        print(tb)

    @staticmethod
    def checkVersion():
        onlineVer = aigpy.pip.getLastVersion('tidal-dl')
        if onlineVer is not None:
            icmp = aigpy.system.cmpVersion(onlineVer, VERSION)
            if icmp > 0:
                Printf.info(LANG.select.PRINT_LATEST_VERSION + ' ' + onlineVer)

    @staticmethod
    def settings():
        data = SETTINGS
        tb = Printf.__gettable__([LANG.select.SETTING, LANG.select.VALUE], [
            #settings - path and format
            [LANG.select.SETTING_PATH, getProfilePath()],
            [LANG.select.SETTING_DOWNLOAD_PATH, data.downloadPath],
            [LANG.select.SETTING_ALBUM_FOLDER_FORMAT, data.albumFolderFormat],
            [LANG.select.SETTING_PLAYLIST_FOLDER_FORMAT, data.playlistFolderFormat],
            [LANG.select.SETTING_TRACK_FILE_FORMAT, data.trackFileFormat],
            [LANG.select.SETTING_VIDEO_FILE_FORMAT, data.videoFileFormat],

            #settings - quality
            [LANG.select.SETTING_AUDIO_QUALITY, data.audioQuality],
            [LANG.select.SETTING_VIDEO_QUALITY, data.videoQuality],

            #settings - else
            [LANG.select.SETTING_USE_PLAYLIST_FOLDER, data.usePlaylistFolder],
            [LANG.select.SETTING_CHECK_EXIST, data.checkExist],
            [LANG.select.SETTING_SHOW_PROGRESS, data.showProgress],
            [LANG.select.SETTING_SHOW_TRACKINFO, data.showTrackInfo],
            [LANG.select.SETTING_SAVE_ALBUMINFO, data.saveAlbumInfo],
            [LANG.select.SETTING_DOWNLOAD_VIDEOS, data.downloadVideos],
            [LANG.select.SETTING_SAVE_COVERS, data.saveCovers],
            [LANG.select.SETTING_INCLUDE_EP, data.includeEP],
            [LANG.select.SETTING_LANGUAGE, LANG.getLangName(data.language)],
            [LANG.select.SETTING_ADD_LRC_FILE, data.lyricFile],
            [LANG.select.SETTING_MULITHREAD_DOWNLOAD, data.multiThread],
            [LANG.select.SETTING_APIKEY, f"[{data.apiKeyIndex}]" + apiKey.getItem(data.apiKeyIndex)['formats']],
            [LANG.select.SETTING_DOWNLOAD_DELAY, data.downloadDelay],
            [LANG.select.SETTING_LISTENER_ENABLED, data.listenerEnabled],
            [LANG.select.SETTING_LISTENER_PORT, data.listenerPort],
            [LANG.select.SETTING_LISTENER_SECRET, Printf._mask_listener_secret(data.listenerSecret)],
        ])
        print(tb)

    @staticmethod
    def choices():
        print("====================================================")
        tb = Printf.__gettable__([LANG.select.CHOICE, LANG.select.FUNCTION], [
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER + " '0':"), LANG.select.CHOICE_EXIT],
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER + " '1':"), LANG.select.CHOICE_LOGIN],
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER + " '2':"), LANG.select.CHOICE_LOGOUT],
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER + " '3':"), LANG.select.CHOICE_SET_ACCESS_TOKEN],
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER + " '4':"), LANG.select.CHOICE_SETTINGS + '-Path'],
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER + " '5':"), LANG.select.CHOICE_SETTINGS + '-Quality'],
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER + " '6':"), LANG.select.CHOICE_SETTINGS + '-Else'],
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER + " '7':"), LANG.select.CHOICE_APIKEY],
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER + " '8':"), LANG.select.CHOICE_PKCE_LOGIN],
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER + " '9':"), LANG.select.CHOICE_LISTENER],
            [aigpy.cmd.green(LANG.select.CHOICE_ENTER_URLID), LANG.select.CHOICE_DOWNLOAD_BY_URL],
        ])
        tb.set_style(prettytable.PLAIN_COLUMNS)
        print(tb)
        print("====================================================")

    @staticmethod
    def enter(string):
        aigpy.cmd.colorPrint(string, aigpy.cmd.TextColor.Yellow, None)
        ret = input("")
        return ret

    @staticmethod
    def enterBool(string):
        aigpy.cmd.colorPrint(string, aigpy.cmd.TextColor.Yellow, None)
        ret = input("")
        return ret == '1'

    @staticmethod
    def enterPath(string, errmsg, retWord='0', default=""):
        while True:
            ret = aigpy.cmd.inputPath(aigpy.cmd.yellow(string), retWord)
            if ret == retWord:
                return default
            elif ret == "":
                print(aigpy.cmd.red(LANG.select.PRINT_ERR + " ") + errmsg)
            else:
                break
        return ret

    @staticmethod
    def enterLimit(string, errmsg, limit=[]):
        while True:
            ret = aigpy.cmd.inputLimit(aigpy.cmd.yellow(string), limit)
            if ret is None:
                print(aigpy.cmd.red(LANG.select.PRINT_ERR + " ") + errmsg)
            else:
                break
        return ret

    @staticmethod
    def enterFormat(string, current, default):
        ret = Printf.enter(string)
        if ret == '0' or aigpy.string.isNull(ret):
            return current
        if ret.lower() == 'default':
            return default
        return ret

    @staticmethod
    def err(string):
        global print_mutex
        print_mutex.acquire()
        print(aigpy.cmd.red(LANG.select.PRINT_ERR + " ") + string)
        # logging.error(string)
        print_mutex.release()

    @staticmethod
    def info(string):
        global print_mutex
        print_mutex.acquire()
        print(aigpy.cmd.blue(LANG.select.PRINT_INFO + " ") + string)
        print_mutex.release()

    @staticmethod
    def success(string):
        global print_mutex
        print_mutex.acquire()
        print(aigpy.cmd.green(LANG.select.PRINT_SUCCESS + " ") + string)
        print_mutex.release()

    @staticmethod
    def album(data: Album):
        tb = Printf.__gettable__([LANG.select.MODEL_ALBUM_PROPERTY, LANG.select.VALUE], [
            [LANG.select.MODEL_TITLE, data.title],
            ["ID", data.id],
            [LANG.select.MODEL_TRACK_NUMBER, data.numberOfTracks],
            [LANG.select.MODEL_VIDEO_NUMBER, data.numberOfVideos],
            [LANG.select.MODEL_RELEASE_DATE, data.releaseDate],
            [LANG.select.MODEL_VERSION, data.version],
            [LANG.select.MODEL_EXPLICIT, data.explicit],
        ])
        print(tb)
        logging.info("====album " + str(data.id) + "====\n" +
                     "title:" + data.title + "\n" +
                     "track num:" + str(data.numberOfTracks) + "\n" +
                     "video num:" + str(data.numberOfVideos) + "\n" +
                     "==================================")

    @staticmethod
    def track(data: Track, stream: StreamUrl = None):
        tb = Printf.__gettable__([LANG.select.MODEL_TRACK_PROPERTY, LANG.select.VALUE], [
            [LANG.select.MODEL_TITLE, data.title],
            ["ID", data.id],
            [LANG.select.MODEL_ALBUM, data.album.title],
            [LANG.select.MODEL_VERSION, data.version],
            [LANG.select.MODEL_EXPLICIT, data.explicit],
            ["Max-Q", data.audioQuality],
        ])
        if stream is not None:
            tb.add_row(["Get-Q", str(stream.soundQuality)])
            tb.add_row(["Get-Codec", str(stream.codec)])
        print(tb)
        logging.info("====track " + str(data.id) + "====\n" + \
                     "title:" + data.title + "\n" + \
                     "version:" + str(data.version) + "\n" + \
                     "==================================")

    @staticmethod
    def video(data: Video, stream: VideoStreamUrl = None):
        tb = Printf.__gettable__([LANG.select.MODEL_VIDEO_PROPERTY, LANG.select.VALUE], [
            [LANG.select.MODEL_TITLE, data.title],
            [LANG.select.MODEL_ALBUM, data.album.title if data.album != None else None],
            [LANG.select.MODEL_VERSION, data.version],
            [LANG.select.MODEL_EXPLICIT, data.explicit],
            ["Max-Q", data.quality],
        ])
        if stream is not None:
            tb.add_row(["Get-Q", str(stream.resolution)])
            tb.add_row(["Get-Codec", str(stream.codec)])
        print(tb)
        logging.info("====video " + str(data.id) + "====\n" +
                     "title:" + data.title + "\n" +
                     "version:" + str(data.version) + "\n" +
                     "==================================")

    @staticmethod
    def artist(data: Artist, num):
        tb = Printf.__gettable__([LANG.select.MODEL_ARTIST_PROPERTY, LANG.select.VALUE], [
            [LANG.select.MODEL_ID, data.id],
            [LANG.select.MODEL_NAME, data.name],
            ["Number of albums", num],
            [LANG.select.MODEL_TYPE, str(data.type)],
        ])
        print(tb)
        logging.info("====artist " + str(data.id) + "====\n" +
                     "name:" + data.name + "\n" +
                     "album num:" + str(num) + "\n" +
                     "==================================")

    @staticmethod
    def playlist(data):
        tb = Printf.__gettable__([LANG.select.MODEL_PLAYLIST_PROPERTY, LANG.select.VALUE], [
            [LANG.select.MODEL_TITLE, data.title],
            [LANG.select.MODEL_TRACK_NUMBER, data.numberOfTracks],
            [LANG.select.MODEL_VIDEO_NUMBER, data.numberOfVideos],
        ])
        print(tb)
        logging.info("====playlist " + str(data.uuid) + "====\n" +
                     "title:" + data.title + "\n" +
                     "track num:" + str(data.numberOfTracks) + "\n" +
                     "video num:" + str(data.numberOfVideos) + "\n" +
                     "==================================")

    @staticmethod
    def mix(data):
        tb = Printf.__gettable__([LANG.select.MODEL_PLAYLIST_PROPERTY, LANG.select.VALUE], [
            [LANG.select.MODEL_ID, data.id],
            [LANG.select.MODEL_TRACK_NUMBER, len(data.tracks)],
            [LANG.select.MODEL_VIDEO_NUMBER, len(data.videos)],
        ])
        print(tb)
        logging.info("====Mix " + str(data.id) + "====\n" +
                     "track num:" + str(len(data.tracks)) + "\n" +
                     "video num:" + str(len(data.videos)) + "\n" +
                     "==================================")

    @staticmethod
    def apikeys(items):
        print("-------------API-KEYS---------------")
        tb = prettytable.PrettyTable()
        tb.field_names = [aigpy.cmd.green('Index'),
                          aigpy.cmd.green('Valid'),
                          aigpy.cmd.green('Platform'),
                          aigpy.cmd.green('Formats'), ]
        tb.align = 'l'

        for index, item in enumerate(items):
            tb.add_row([str(index),
                        aigpy.cmd.green('True') if item["valid"] == "True" else aigpy.cmd.red('False'),
                        item["platform"],
                        item["formats"]])
        print(tb)
