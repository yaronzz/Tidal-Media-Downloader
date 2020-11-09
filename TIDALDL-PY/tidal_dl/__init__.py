#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/06
@Author  :   Yaronzz
@Version :   2.0
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

from tidal_dl.tidal import TidalAPI
from tidal_dl.settings import Settings, UserSettings
from tidal_dl.printf import Printf, VERSION
from tidal_dl.download import start
from tidal_dl.enum import AudioQuality, VideoQuality
from tidal_dl.lang.language import getLang, setLang, initLang

ssl._create_default_https_context = ssl._create_unverified_context

API = TidalAPI()
USER = UserSettings.read()
CONF = Settings.read()
LANG = initLang(CONF.language)

def displayTime(seconds, granularity=2):
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
    
    print(LANG.AUTH_LOGIN_CODE.format(API.key.userCode))
    print(LANG.AUTH_NEXT_STEP.format(API.key.verificationUrl, displayTime(API.key.authCheckTimeout)))
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
            USER.userid = API.key.userId
            USER.countryCode = API.key.countryCode
            USER.accessToken = API.key.accessToken
            USER.refreshToken = API.key.refreshToken
            USER.expiresAfter = time.time() + int(API.key.expiresIn)
            UserSettings.save(USER)
            break
    if elapsed >= API.key.authCheckTimeout:
    	Printf.err(LANG.AUTH_TIMEOUT)
    return

def checkLogin():
    if not isNull(USER.accessToken):
        #print('Checking Access Token...') #add to translations
        msg, check = API.verifyAccessToken(USER.accessToken)
        if check == True:
            Printf.info(LANG.MSG_VALID_ACCESSTOKEN.format(displayTime(int(USER.expiresAfter - time.time()))))
            return
        else:
            Printf.info(LANG.MSG_INVAILD_ACCESSTOKEN)
            msg, check = API.refreshAccessToken(USER.refreshToken)
            if check == True:
                Printf.success(LANG.MSG_VALID_ACCESSTOKEN.format(displayTime(int(API.key.expiresIn))))
                USER.userid = API.key.userId
                USER.countryCode = API.key.countryCode
                USER.accessToken = API.key.accessToken
                USER.expiresAfter = time.time() + int(API.key.expiresIn)
                UserSettings.save(USER)
                return
            else:
                Printf.err(msg)
                tmp = UserSettings()	#clears saved tokens
                UserSettings.save(tmp)
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
    if albumFolderFormat == '0':
        albumFolderFormat = CONF.albumFolderFormat
    else:
        CONF.albumFolderFormat = albumFolderFormat
    trackFileFormat = Printf.enter(LANG.CHANGE_TRACK_FILE_FORMAT)
    if trackFileFormat == '0':
        trackFileFormat = CONF.trackFileFormat
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
            start(USER, CONF, val)
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
        else:
            start(USER, CONF, choice)

if __name__ == "__main__":
    main()
    # test example
    # track 70973230 
    # video 155608351
    # album 58138532  77803199  21993753   79151897  56288918
