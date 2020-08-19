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
from aigpy.stringHelper import isNull
from aigpy.pathHelper import mkdirs
from aigpy.pipHelper import getLastVersion
from aigpy.versionHelper import cmpVersion
from tidal_dl.tidal import TidalAPI
from tidal_dl.settings import Settings, UserSettings
from tidal_dl.printf import Printf, VERSION
from tidal_dl.download import start
from tidal_dl.enum import AudioQuality, VideoQuality

API = TidalAPI()
USER = UserSettings.read()
CONF = Settings.read()
TOKEN1,TOKEN2 = API.getToken()



def login(username="", password=""):
    while True:
        if isNull(username) or isNull(password):
            print("----------------LogIn------------------")
            username = Printf.enter("username:")
            password = Printf.enter("password:")
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
        msg, check = API.loginByAccessToken(token)
        if check == False:
            Printf.err(msg)
            continue
        if USER.userid != API.key.userId:
            Printf.err("User mismatch! Please use your own accesstoken.")
            continue
        break

    USER.assesstoken = token
    UserSettings.save(USER)



def checkLogin():
    if not isNull(USER.assesstoken):
        mag, check = API.loginByAccessToken(USER.assesstoken)
        if check == False:
            Printf.err("Invaild AccessToken!Please reset.")
    if not isNull(USER.sessionid1) and not API.isValidSessionID(USER.userid, USER.sessionid1):
        USER.sessionid1 = ""
    if not isNull(USER.sessionid2) and API.isValidSessionID(USER.userid, USER.sessionid2):
        USER.sessionid2 = ""
    if isNull(USER.sessionid1) or isNull(USER.sessionid2):
        login(USER.username, USER.password)



def changeSettings():
    Printf.settings(CONF)
    while True:
        choice = Printf.enter("Download path('0' not modify):")
        if choice == '0':
            choice = CONF.downloadPath
        elif not os.path.isdir(choice):
            if not mkdirs(choice):
                Printf.err('Path is error!')
                continue
        CONF.downloadPath = choice
        break
    while True:
        choice = Printf.enter("Audio quailty('0'-Normal,'1'-High,'2'-HiFi,'3'-Master):")
        if choice != '1' and choice != '2' and choice != '3' and choice != '0':
            Printf.err('Input error!')
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
        choice = Printf.enter("Video quailty('0'-1080,'1'-720,'2'-480,'3'-360):")
        if choice != '1' and choice != '2' and choice != '3' and choice != '0':
            Printf.err('Input error!')
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
    CONF.onlyM4a = Printf.enter("Convert mp4 to m4a('0'-No,'1'-Yes):") == '1'
    CONF.addExplicitTag = Printf.enter("Add explicit tag to file names('0'-No,'1'-Yes):") == '1'
    CONF.addHyphen = Printf.enter("Use hyphens instead of spaces in file names('0'-No,'1'-Yes):") == '1'
    CONF.addYear = Printf.enter("Add year to album folder names('0'-No,'1'-Yes):") == '1'
    CONF.useTrackNumber = Printf.enter("Add track number before file names('0'-No,'1'-Yes):") == '1'
    CONF.checkExist = Printf.enter("Check exist file befor download track('0'-No,'1'-Yes):") == '1'
    CONF.artistBeforeTitle = Printf.enter("Add artistName before track title('0'-No,'1'-Yes):") == '1'
    CONF.includeEP = Printf.enter("Include singles and EPs when downloading an artist's albums('0'-No,'1'-Yes):") == '1'
    CONF.addAlbumIDBeforeFolder = Printf.enter("Add id before album folder('0'-No,'1'-Yes):") == '1'
    CONF.saveCovers = Printf.enter("Save covers('0'-No,'1'-Yes):") == '1'
    Settings.save(CONF)


def main():
    Printf.logo()
    Printf.settings(CONF)
    checkLogin()

    onlineVer = getLastVersion('tidal-dl')
    if not isNull(onlineVer):
        icmp = cmpVersion(onlineVer, VERSION)
        if icmp > 0:
            Printf.info('Latest version: ' + onlineVer)

    while True:
        Printf.choices()
        choice = Printf.enter("Enter Choice:")
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



