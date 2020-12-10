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
from aigpy.versionHelper import cmpVersion
from aigpy.cmdHelper import red, green, blue, yellow, TextColor

from tidal_dl.tidal import TidalAPI
from tidal_dl.settings import Settings, TokenSettings
from tidal_dl.printf import Printf, VERSION
from tidal_dl.download import start, test
from tidal_dl.enum import AudioQuality, VideoQuality
from tidal_dl.lang.language import getLang, setLang, initLang

ssl._create_default_https_context = ssl._create_unverified_context

API   = TidalAPI()
TOKEN = TokenSettings.read()
CONF  = Settings.read()
LANG  = initLang(CONF.language)

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
        msg, check = API.checkAuthStatus()
        if check == False:
            if msg == "pending":
                time.sleep(API.key.authCheckInterval)
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
        #print('Checking Access Token...') #add to translations
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
                tmp = TokenSettings()	#clears saved tokens
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

    while True:
        choice = Printf.enter(LANG.CHANGE_DOWNLOAD_PATH)
        if choice == '0':
            choice = CONF.downloadPath
        elif not os.path.isdir(choice):
            if not mkdirs(choice):
                Printf.err(LANG.MSG_PATH_ERR)
                continue
        CONF.downloadPath = choice
        break
    while True:
        choice = Printf.enter(LANG.CHANGE_AUDIO_QUALITY)
        if choice != '1' and choice != '2' and choice != '3' and choice != '0':
            Printf.err(LANG.MSG_INPUT_ERR)
            continue
        if choice == '0':
            CONF.audioQuality = AudioQuality.Normal
        if choice == '1':
            CONF.audioQuality = AudioQuality.High
        if choice == '2':
            CONF.audioQuality = AudioQuality.HiFi
        if choice == '3':
            CONF.audioQuality = AudioQuality.Master
        break
    while True:
        choice = Printf.enter(LANG.CHANGE_VIDEO_QUALITY)
        if choice != '1' and choice != '2' and choice != '3' and choice != '0':
            Printf.err(LANG.MSG_INPUT_ERR)
            continue
        if choice == '0':
            CONF.videoQuality = VideoQuality.P1080
        if choice == '1':
            CONF.videoQuality = VideoQuality.P720
        if choice == '2':
            CONF.videoQuality = VideoQuality.P480
        if choice == '3':
            CONF.videoQuality = VideoQuality.P360
        break
    CONF.onlyM4a = Printf.enter(LANG.CHANGE_ONLYM4A) == '1'
    # CONF.addExplicitTag = Printf.enter(LANG.CHANGE_ADD_EXPLICIT_TAG) == '1'
    # CONF.addHyphen = Printf.enter(LANG.CHANGE_ADD_HYPHEN) == '1'
    # CONF.addYear = Printf.enter(LANG.CHANGE_ADD_YEAR) == '1'
    # CONF.useTrackNumber = Printf.enter(LANG.CHANGE_USE_TRACK_NUM) == '1'
    CONF.checkExist = Printf.enter(LANG.CHANGE_CHECK_EXIST) == '1'
    # CONF.artistBeforeTitle = Printf.enter(LANG.CHANGE_ARTIST_BEFORE_TITLE) == '1'
    CONF.includeEP = Printf.enter(LANG.CHANGE_INCLUDE_EP) == '1'
    # CONF.addAlbumIDBeforeFolder = Printf.enter(LANG.CHANGE_ALBUMID_BEFORE_FOLDER) == '1'
    CONF.saveCovers = Printf.enter(LANG.CHANGE_SAVE_COVERS) == '1'
    CONF.showProgress = Printf.enter(LANG.CHANGE_SHOW_PROGRESS) == '1'
    CONF.language = Printf.enter(LANG.CHANGE_LANGUAGE +
                                 "('0'-English,'1'-中文,'2'-Turkish,'3'-Italiano,'4'-Czech,'5'-Arabic,'6'-Russian,'7'-Filipino,'8'-Croatian,'9'-Spanish,'10'-Portuguese,'11'-Ukrainian,'12'-Vietnamese,'13'-French,'14'-German):")
    albumFolderFormat = Printf.enter(LANG.CHANGE_ALBUM_FOLDER_FORMAT)
    if albumFolderFormat == '0' or isNull(albumFolderFormat):
        pass
    elif albumFolderFormat.lower() == 'default':
        CONF.albumFolderFormat = Settings.getDefaultAlbumFolderFormat()
    else:
        CONF.albumFolderFormat = albumFolderFormat
    trackFileFormat = Printf.enter(LANG.CHANGE_TRACK_FILE_FORMAT)
    if trackFileFormat == '0' or isNull(trackFileFormat):
        pass
    elif trackFileFormat.lower() == "default":
        CONF.trackFileFormat = Settings.getDefaultAlbumFolderFormat()
    else:
        CONF.trackFileFormat = trackFileFormat

    LANG = setLang(CONF.language)
    Settings.save(CONF)


def mainCommand():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvl:o:q:r:", ["help", "version", "link=", "output=", "quality", "resolution"])
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
