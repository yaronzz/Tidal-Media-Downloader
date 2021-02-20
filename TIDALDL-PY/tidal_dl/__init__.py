#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   2.1
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import logging
import os
import requests
import prettytable
import ssl
import sys
import getopt
import time

from aigpy.stringHelper import isNull
from aigpy.pathHelper import mkdirs
from aigpy.pipHelper import getLastVersion
from aigpy.systemHelper import cmpVersion
from aigpy.cmdHelper import red, green, blue, yellow, TextColor

from tidal_dl.tidal import TidalAPI
from tidal_dl.settings import Settings, TokenSettings, getLogPath
from tidal_dl.printf import Printf, VERSION
from tidal_dl.download import start
from tidal_dl.enum import AudioQuality, VideoQuality
from tidal_dl.lang.language import getLang, setLang, initLang, getLangChoicePrint

ssl._create_default_https_context = ssl._create_unverified_context

API = TidalAPI()
TOKEN = TokenSettings.read()
CONF = Settings.read()
LANG = initLang(CONF.language)

logging.basicConfig(filename=getLogPath(),
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


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


def login():
    print(LANG.AUTH_START_LOGIN)
    msg, check = API.getDeviceCode()
    if check == False:
        Printf.err(msg)
        return

    print(LANG.AUTH_LOGIN_CODE.format(green(API.key.userCode)))
    print(LANG.AUTH_NEXT_STEP.format(green(API.key.verificationUrl), yellow(displayTime(API.key.authCheckTimeout))))
    print(LANG.AUTH_WAITING)
    start = time.time()
    elapsed = 0
    while elapsed < API.key.authCheckTimeout:
        elapsed = time.time() - start
        # print("Check auth status...")
        msg, check = API.checkAuthStatus()
        if check == False:
            if msg == "pending":
                time.sleep(API.key.authCheckInterval + 1)
                continue
            Printf.err(msg)
            break
        if check == True:
            Printf.success(LANG.MSG_VALID_ACCESSTOKEN.format(displayTime(int(API.key.expiresIn))))
            TOKEN.userid = API.key.userId
            TOKEN.countryCode = API.key.countryCode
            TOKEN.accessToken = API.key.accessToken
            TOKEN.refreshToken = API.key.refreshToken
            TOKEN.expiresAfter = time.time() + int(API.key.expiresIn)
            TokenSettings.save(TOKEN)
            break
    if elapsed >= API.key.authCheckTimeout:
        Printf.err(LANG.AUTH_TIMEOUT)
    return


def setAccessToken():
    while True:
        print("-------------AccessToken---------------")
        token = Printf.enter("accessToken('0' go back):")
        if token == '0':
            return
        msg, check = API.loginByAccessToken(token, TOKEN.userid)
        if check == False:
            Printf.err(msg)
            continue
        break

    print("-------------RefreshToken---------------")
    refreshToken = Printf.enter("refreshToken('0' to skip):")
    if refreshToken == '0':
        refreshToken = TOKEN.refreshToken

    TOKEN.assesstoken = token
    TOKEN.refreshToken = refreshToken
    TOKEN.expiresAfter = 0
    TokenSettings.save(TOKEN)


def checkLogin():
    if not isNull(TOKEN.accessToken):
        # print('Checking Access Token...') #add to translations
        msg, check = API.verifyAccessToken(TOKEN.accessToken)
        if check == True:
            Printf.info(LANG.MSG_VALID_ACCESSTOKEN.format(displayTime(int(TOKEN.expiresAfter - time.time()))))
            return
        else:
            Printf.info(LANG.MSG_INVAILD_ACCESSTOKEN)
            msg, check = API.refreshAccessToken(TOKEN.refreshToken)
            if check == True:
                Printf.success(LANG.MSG_VALID_ACCESSTOKEN.format(displayTime(int(API.key.expiresIn))))
                TOKEN.userid = API.key.userId
                TOKEN.countryCode = API.key.countryCode
                TOKEN.accessToken = API.key.accessToken
                TOKEN.expiresAfter = time.time() + int(API.key.expiresIn)
                TokenSettings.save(TOKEN)
                return
            else:
                Printf.err(msg)
                tmp = TokenSettings()  # clears saved tokens
                TokenSettings.save(tmp)
    login()
    return


def checkLogout():
    global LANG
    login()
    return


def changeSettings():
    global LANG
    Printf.settings(CONF)
    choice = Printf.enter(LANG.CHANGE_START_SETTINGS)
    if choice == '0':
        return

    CONF.downloadPath = Printf.enterPath(LANG.CHANGE_DOWNLOAD_PATH, LANG.MSG_PATH_ERR, '0', CONF.downloadPath)
    CONF.audioQuality = AudioQuality(int(Printf.enterLimit(
        LANG.CHANGE_AUDIO_QUALITY, LANG.MSG_INPUT_ERR, ['0', '1', '2', '3'])))
    CONF.videoQuality = AudioQuality(int(Printf.enterLimit(
        LANG.CHANGE_VIDEO_QUALITY, LANG.MSG_INPUT_ERR, ['0', '1', '2', '3'])))
    CONF.onlyM4a = Printf.enter(LANG.CHANGE_ONLYM4A) == '1'
    CONF.checkExist = Printf.enter(LANG.CHANGE_CHECK_EXIST) == '1'
    CONF.includeEP = Printf.enter(LANG.CHANGE_INCLUDE_EP) == '1'
    CONF.saveCovers = Printf.enter(LANG.CHANGE_SAVE_COVERS) == '1'
    CONF.showProgress = Printf.enter(LANG.CHANGE_SHOW_PROGRESS) == '1'
    CONF.language = Printf.enter(LANG.CHANGE_LANGUAGE + "(" + getLangChoicePrint() + "):")
    CONF.albumFolderFormat = Printf.enterFormat(
        LANG.CHANGE_ALBUM_FOLDER_FORMAT, CONF.albumFolderFormat, Settings.getDefaultAlbumFolderFormat())
    CONF.trackFileFormat = Printf.enterFormat(LANG.CHANGE_TRACK_FILE_FORMAT,
                                              CONF.trackFileFormat, Settings.getDefaultTrackFileFormat())

    LANG = setLang(CONF.language)
    Settings.save(CONF)


def mainCommand():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvl:o:q:r:", ["help", "version",
                                                                "link=", "output=", "quality", "resolution"])
    except getopt.GetoptError as errmsg:
        Printf.err(vars(errmsg)['msg'] + ". Use 'tidal-dl -h' for useage.")
        return

    for opt, val in opts:
        if opt in ('-h', '--help'):
            Printf.usage()
            return
        if opt in ('-v', '--version'):
            Printf.logo()
            return
        if opt in ('-l', '--link'):
            checkLogin()
            start(TOKEN, CONF, val)
            return
        if opt in ('-o', '--output'):
            CONF.downloadPath = val
            Settings.save(CONF)
            return
        if opt in ('-q', '--quality'):
            CONF.audioQuality = Settings.getAudioQuality(val)
            Settings.save(CONF)
            return
        if opt in ('-r', '--resolution'):
            CONF.videoQuality = Settings.getVideoQuality(val)
            Settings.save(CONF)
            return

        if not mkdirs(CONF.downloadPath):
            Printf.err(LANG.MSG_PATH_ERR + CONF.downloadPath)
            return


def main():
    if len(sys.argv) > 1:
        mainCommand()
        return

    Printf.logo()
    Printf.settings(CONF)

    checkLogin()

    onlineVer = getLastVersion('tidal-dl')
    if not isNull(onlineVer):
        icmp = cmpVersion(onlineVer, VERSION)
        if icmp > 0:
            Printf.info(LANG.PRINT_LATEST_VERSION + ' ' + onlineVer)

    while True:
        Printf.choices()
        choice = Printf.enter(LANG.PRINT_ENTER_CHOICE)
        if choice == "0":
            return
        elif choice == "1":
            checkLogin()
        elif choice == "2":
            changeSettings()
        elif choice == "3":
            checkLogout()
        elif choice == "4":
            setAccessToken()
        else:
            start(TOKEN, CONF, choice)


if __name__ == "__main__":
    main()
    # test example
    # track 70973230  77798028
    # video 155608351
    # album 58138532  77803199  21993753   79151897  56288918
