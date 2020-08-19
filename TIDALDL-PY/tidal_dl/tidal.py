#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tidal.py
@Time    :   2019/02/27
@Author  :   Yaronzz
@VERSION :   2.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   tidal api
'''
import os
import re
import uuid
import requests
import json
import base64
import aigpy.stringHelper as stringHelper
from aigpy.modelHelper import dictToModel
from aigpy.stringHelper import isNull
from tidal_dl.model import Album, Track, Video, Artist, Playlist, StreamUrl, VideoStreamUrl
from tidal_dl.enum import Type, AudioQuality, VideoQuality

__VERSION__ = '1.9.1'
__URL_PRE__ = 'https://api.tidalhifi.com/v1/'

class LoginKey(object):
    def __init__(self):
        self.username = ""
        self.password = ""
        self.userId = ""
        self.countryCode = ""
        self.sessionId = ""
        self.accessToken = ""


class __StreamRespon__(object):
    trackid = None
    videoid = None
    streamType = None
    assetPresentation = None
    audioMode = None
    audioQuality = None
    videoQuality = None
    manifestMimeType = None
    manifest = None



class TidalAPI(object):
    def __init__(self):
        self.key = LoginKey()

    def __get__(self, path, params={}, retry=3):
        header = {'X-Tidal-SessionId': self.key.sessionId}
        if not isNull(self.key.accessToken):
            header = {'authorization': 'Bearer {}'.format(self.key.accessToken)}

        params['countryCode'] = self.key.countryCode
        result = requests.get(__URL_PRE__ + path,  headers=header, params=params).json()
        if 'status' in result:
            if 'userMessage' in result and result['userMessage'] is not None:
                return result['userMessage'], None
            else:
                return "Get operation err!", None
        return None, result

    def __getItems__(self, path, params={}, retry = 3):
        params['limit'] = 50
        params['offset'] = 0
        ret = []
        while True:
            msg, data = self.__get__(path, params, retry)
            if msg is not None:
                return msg, None
            num = 0
            for item in data["items"]:
                num += 1
                ret.append(item)
            if num < 50:
                break
            params['offset'] += num
        return None, ret

    def __getQualityString__(self, quality:AudioQuality):
        if quality == AudioQuality.Normal:
            return "LOW"
        if quality == AudioQuality.High:
            return "HIGH"
        if quality == AudioQuality.HiFi:
            return "LOSSLESS"
        return "HI_RES"
    
    def __getResolutionList__(self, url):
        ret = []
        txt = requests.get(url).text
        array = txt.split("#EXT-X-STREAM-INF")
        for item in array:
            if "RESOLUTION=" not in item:
                continue
            stream = VideoStreamUrl()
            stream.codec = stringHelper.getSub(item, "CODECS=\"", "\"")
            stream.m3u8Url = "http" + stringHelper.getSubOnlyStart(item, "http").strip()
            stream.resolution = stringHelper.getSub(item, "RESOLUTION=", "http").strip()
            stream.resolutions = stream.resolution.split("x")
            ret.append(stream)
        return ret

    def login(self, username, password, token):
        data = {
            'username': username,
            'password': password,
            'token': token,
            'clientUniqueKey': str(uuid.uuid4()).replace('-', '')[16:],
            'client__VERSION__': __VERSION__
            }
        result = requests.post(__URL_PRE__ + 'login/username', data=data).json()
        if 'status' in result:
            if 'userMessage' in result and result['userMessage'] is not None:
                return result['userMessage'], False
            else:
                return "Login failed!", False

        self.key.username = username
        self.key.password = password
        self.key.userId = result['userId']
        self.key.countryCode = result['countryCode']
        self.key.sessionId = result['sessionId']
        return None, True
    
    def loginByAccessToken(self, accessToken, userid = None):
        header = {'authorization': 'Bearer {}'.format(accessToken)}
        result = requests.get('https://api.tidal.com/v1/sessions', headers=header).json()
        if 'status' in result and result['status'] != 200:
            return "Login failed!", False

        if not isNull(userid):
            if str(result['userId']) != str(userid):
                return "User mismatch! Please use your own accesstoken.", False

        self.key.userId = result['userId']
        self.key.countryCode = result['countryCode']
        self.key.accessToken = accessToken
        return None, True

    def isValidSessionID(self, userId, sessionId):
        params = {'sessionId': sessionId}
        result = requests.get(__URL_PRE__ + 'users/' + str(userId), params=params).json()
        if 'status' in result and not result['status'] == 200:
            return False
        return True

    def getAlbum(self, id):
        msg, data = self.__get__('albums/' + str(id))
        return msg, dictToModel(data, Album())

    def getPlaylist(self, id):
        msg, data = self.__get__('playlists/' + str(id))
        return msg, dictToModel(data, Playlist())

    def getArtist(self, id):
        msg, data = self.__get__('artists/' + str(id))
        return msg, dictToModel(data, Artist())

    def getTrack(self, id):
        msg, data = self.__get__('tracks/' + str(id))
        return msg, dictToModel(data, Track())

    def getVideo(self, id):
        msg, data = self.__get__('videos/' + str(id))
        return msg, dictToModel(data, Video())

    def getItems(self, id, type:Type):
        if type == Type.Playlist:
            msg, data = self.__getItems__('playlists/' + str(id) + "/items")
        elif type == Type.Album:
            msg, data = self.__getItems__('albums/' + str(id) + "/items")
        else:
            return "invalid Type!", None, None
        if msg is not None:
            return msg, None, None
        tracks = []
        videos = []
        for item in data:
            if item['type'] == 'track':
                tracks.append(dictToModel(item['item'], Track()))
            else:
                videos.append(dictToModel(item['item'], Video()))
        return msg, tracks, videos

    def getArtistAlbums(self, id, includeEP = False):
        albums = []
        msg, data = self.__getItems__('artists/' + str(id) + "/albums")
        if msg is not None:
            return msg, None
        for item in data:
            albums.append(dictToModel(item, Album()))
        if includeEP == False:
            return None, albums
        msg, data = self.__getItems__('artists/' + str(id) + "/albums", {"filter": "EPSANDSINGLES"})
        if msg is not None:
            return msg, None
        for item in data:
            albums.append(dictToModel(item, Album()))
        return None, albums

    def getStreamUrl(self, id, quality: AudioQuality):
        squality = self.__getQualityString__(quality)
        paras = {"audioquality": squality, "playbackmode": "STREAM", "assetpresentation": "FULL"}
        msg, data = self.__get__('tracks/' + str(id) + "/playbackinfopostpaywall", paras)
        if msg is not None:
            return msg, None
        resp = dictToModel(data, __StreamRespon__())
        
        if "vnd.tidal.bt" in resp.manifestMimeType:
            manifest = json.loads(base64.b64decode(resp.manifest).decode('utf-8'))
            ret = StreamUrl()
            ret.trackid = resp.trackid
            ret.soundQuality = resp.audioQuality
            ret.codec = manifest['codecs']
            ret.encryptionKey = manifest['keyId'] if 'keyId' in manifest else ""
            ret.url = manifest['urls'][0]
            return "", ret
        return "", None

    def getVideoStreamUrl(self, id, quality: VideoQuality):
        paras = {"videoquality": "HIGH", "playbackmode": "STREAM", "assetpresentation": "FULL"}
        msg, data = self.__get__('videos/' + str(id) + "/playbackinfopostpaywall", paras)
        if msg is not None:
            return msg, None
        resp = dictToModel(data, __StreamRespon__())
        
        if "vnd.tidal.emu" in resp.manifestMimeType:
            manifest = json.loads(base64.b64decode(resp.manifest).decode('utf-8'))
            array = self.__getResolutionList__(manifest['urls'][0])
            icmp = int(quality.value)
            index = 0
            for item in array:
                if icmp >= int(item.resolutions[1]):
                    break
                index += 1
            if index >= len(array):
                index = len(array) - 1
            return "", array[index]
        return "", None
        
    def getCoverUrl(self, sid, width="320", height="320"):
        return "https://resources.tidal.com/images/" + sid.replace("-", "/") + "/" + width + "x" + height + ".jpg"

    def getArtistsName(self, artists = []):
        array = []
        for item in artists:
            array.append(item.name)
        return " / ".join(array)

    def getFlag(self, data, type : Type, short = True, separator = " / "):
        master = False
        explicit = False
        if type == Type.Album or type == Type.Track:
            if data.audioQuality == "HI_RES":
                master = True
            if data.explicit == True:
                explicit = True
        if type == Type.Video:
            if data.explicit == True:
                explicit = True
        if master == False and explicit == False:
            return ""
        array = []
        if master:
            array.append("M" if short else "Master")
        if explicit:
            array.append("E" if short else "Explicit")
        return separator.join(array)

    def parseUrl(self, url):
        etype = Type.Null
        sid = ""
        if "tidal.com" not in url:
            return etype, sid

        url = url.lower()
        if 'artist' in url:
            etype = Type.Artist
        if 'album' in url:
            etype = Type.Album
        if 'track' in url:
            etype = Type.Track
        if 'video' in url:
            etype = Type.Video
        if 'playlist' in url:
            etype = Type.Playlist
        
        if etype == Type.Null:
            return etype, sid

        sid = stringHelper.getSub(url, etype.name.lower() + '/', '/')
        return etype, sid

    def getByString(self, string):
        etype = Type.Null
        obj = None

        if isNull(string):
            return "Please enter something.", etype, obj
        etype, sid = self.parseUrl(string)
        if isNull(sid):
            sid = string

        if obj is None and (etype == Type.Null or etype == Type.Album):
            msg, obj = self.getAlbum(sid)
        if obj is None and (etype == Type.Null or etype == Type.Artist):
            msg, obj = self.getArtist(sid)
        if obj is None and (etype == Type.Null or etype == Type.Track):
            msg, obj = self.getTrack(sid)
        if obj is None and (etype == Type.Null or etype == Type.Video):
            msg, obj = self.getVideo(sid)
        if obj is None and (etype == Type.Null or etype == Type.Playlist):
            msg, obj = self.getPlaylist(sid)

        if obj is None or etype != Type.Null:
            return msg, etype, obj
        if obj.__class__ == Album:
            etype = Type.Album
        if obj.__class__ == Artist:
            etype = Type.Artist
        if obj.__class__ == Track:
            etype = Type.Track
        if obj.__class__ == Video:
            etype = Type.Video
        if obj.__class__ == Playlist:
            etype = Type.Playlist
        return msg, etype, obj

    def getToken(self):
        token1 = "MbjR4DLXz1ghC4rV"    
        token2 = "pl4Vc0hemlAXD0mN"    # only lossless
        try:
            msg = requests.get( "https://cdn.jsdelivr.net/gh/yaronzz/CDN@latest/app/tidal/tokens.json", timeout=(20.05, 27.05))
            tokens = json.loads(msg.text)
            token1 = tokens['token']
            token2 = tokens['token2']
        except Exception as e:
            pass
        return token1,token2
