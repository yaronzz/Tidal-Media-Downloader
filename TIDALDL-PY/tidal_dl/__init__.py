#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/08/15
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import os
import requests
import prettytable
import ssl
import sys
import getopt

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
TOKEN1, TOKEN2 = API.getToken()
LANG = initLang(CONF.language)

def login(username="", password=""):
    while True:
        if isNull(username) or isNull(password):
            print("---------------" + LANG.CHOICE_LOGIN + "-----------------")
            username = Printf.enter(LANG.PRINT_USERNAME)
            password = Printf.enter(LANG.PRINT_PASSWORD)
        msg, check = API.login(username, password, TOKEN1)
        if check == False:
            Printf.err(msg)
            username = ""
            password = ""
            continue
        api2 = TidalAPI()
        msg, check = api2.login(username, password, TOKEN2)
        break
    
    USER.username = username
    USER.password = password
    USER.userid = API.key.userId
    USER.countryCode = API.key.countryCode
    USER.sessionid1 = API.key.sessionId
    USER.sessionid2 = api2.key.sessionId
    UserSettings.save(USER)



def setAccessToken():
    while True:
        print("-------------AccessToken---------------")
        token = Printf.enter("accessToken('0' go back):")
        if token == '0':
            return
        msg, check = API.loginByAccessToken(token, USER.userid)
        if check == False:
            Printf.err(msg)
            continue
        break

    USER.assesstoken = token
    UserSettings.save(USER)



def checkLogin():
    if not isNull(USER.assesstoken):
        mag, check = API.loginByAccessToken(USER.assesstoken)
        if check == False:
            Printf.err(LANG.MSG_INVAILD_ACCESSTOKEN)
    if not isNull(USER.sessionid1) and not API.isValidSessionID(USER.userid, USER.sessionid1):
        USER.sessionid1 = ""
    if not isNull(USER.sessionid2) and API.isValidSessionID(USER.userid, USER.sessionid2):
        USER.sessionid2 = ""
    if isNull(USER.sessionid1) or isNull(USER.sessionid2):
        login(USER.username, USER.password)



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
    CONF.addExplicitTag = Printf.enter(LANG.CHANGE_ADD_EXPLICIT_TAG) == '1'
    CONF.addHyphen = Printf.enter(LANG.CHANGE_ADD_HYPHEN) == '1'
    CONF.addYear = Printf.enter(LANG.CHANGE_ADD_YEAR) == '1'
    CONF.useTrackNumber = Printf.enter(LANG.CHANGE_USE_TRACK_NUM) == '1'
    CONF.checkExist = Printf.enter(LANG.CHANGE_CHECK_EXIST) == '1'
    CONF.artistBeforeTitle = Printf.enter(LANG.CHANGE_ARTIST_BEFORE_TITLE) == '1'
    CONF.includeEP = Printf.enter(LANG.CHANGE_INCLUDE_EP) == '1'
    CONF.addAlbumIDBeforeFolder = Printf.enter(LANG.CHANGE_ALBUMID_BEFORE_FOLDER) == '1'
    CONF.saveCovers = Printf.enter(LANG.CHANGE_SAVE_COVERS) == '1'
    CONF.language = Printf.enter(LANG.CHANGE_LANGUAGE +
                                 "('0'-English,'1'-中文,'2'-Turkish,'3'-Italiano,'4'-Czech,'5'-Arabic,'6'-Russian,'7'-Filipino,'8'-Croatian,'9'-Spanish,'10'-Portuguese):")

    LANG = setLang(CONF.language)
    Settings.save(CONF)


def mainCommand():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:l:v", ["help", "output=","link=","version"]) 
        link = None
        for opt, val in opts:
            if opt in ('-h', '--help'):
                Printf.usage()
                return
            if opt in ('-v', '--version'):
                Printf.logo()
                return
            if opt in ('-l', '--link'):
                link = val
            if opt in ('-o', '--output'):
                CONF.downloadPath = val
        if link is None:
            Printf.err("Please enter the link(url/id/path)! Enter 'tidal-dl -h' for help!");
            return
        if not mkdirs(CONF.downloadPath):
            Printf.err(LANG.MSG_PATH_ERR + CONF.downloadPath)
            return

        checkLogin()
        start(USER, CONF, link)
        return
    except getopt.GetoptError:
        Printf.err("Argv error! Enter 'tidal -h' for help!");

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
            login()
        elif choice == "2":
            changeSettings()
        elif choice == "3":
            setAccessToken()
        else:
            start(USER, CONF, choice)

if __name__ == "__main__":
    main()
    # test example
    # track 70973230 

