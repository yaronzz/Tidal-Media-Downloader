#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   settings.py
@Time    :   2020/08/15
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import json
import base64
from aigpy.fileHelper import getFileContent, write
from aigpy.modelHelper import dictToModel, modelToDict
from tidal_dl.enum import AudioQuality, VideoQuality



def __encode__(string):
    sw = bytes(string, 'utf-8')
    st = base64.b64encode(sw)
    return st

def __decode__(string):
    try:
        sr = base64.b64decode(string)
        st = sr.decode()
        return st
    except:
        return string

class UserSettings(object):
    userid = None
    username = None
    password = None
    sessionid1 = None
    sessionid2 = None
    countryCode = None
    assesstoken = None

    @staticmethod
    def read():
        txt = getFileContent('./usersettings.json', True)
        if txt == "":
            return UserSettings()
        txt = __decode__(txt)
        data = json.loads(txt)
        ret = dictToModel(data, UserSettings())
        return ret
    
    @staticmethod
    def save(model):
        data = modelToDict(model)
        txt = json.dumps(data)
        txt = __encode__(txt)
        write('./usersettings.json', txt, 'wb')

class Settings(object):
    downloadPath = "./download/"
    onlyM4a = False
    addExplicitTag = True
    addHyphen = True
    addYear = False
    useTrackNumber = True
    audioQuality = AudioQuality.Normal
    videoQuality = VideoQuality.P360
    checkExist = True
    artistBeforeTitle = False
    includeEP = True
    addAlbumIDBeforeFolder = False
    saveCovers = True
    language = 0

    @staticmethod
    def read():
        txt = getFileContent('./settings.json')
        if txt == "":
            return Settings()
        data = json.loads(txt)
        ret = dictToModel(data, Settings())
        ret.audioQuality = Settings.getAudioQuality(ret.audioQuality)
        ret.videoQuality = Settings.getVideoQuality(ret.videoQuality)
        return ret

    @staticmethod
    def save(model):
        data = modelToDict(model)
        data['audioQuality'] = model.audioQuality.name
        data['videoQuality'] = model.videoQuality.name
        txt = json.dumps(data)
        write('./settings.json', txt, 'w+')

    @staticmethod
    def getAudioQuality(value):
        for item in AudioQuality:
            if item.name == value:
                return item
        return AudioQuality.Normal

    @staticmethod
    def getVideoQuality(value):
        for item in VideoQuality:
            if item.name == value:
                return item
        return VideoQuality.P360

