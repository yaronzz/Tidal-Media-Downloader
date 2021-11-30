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
import base64
import json
import logging

import aigpy.stringHelper as stringHelper
import requests
from aigpy.modelHelper import dictToModel
from aigpy.stringHelper import isNull
from requests.packages import urllib3
from tidal_dl.enums import Type, AudioQuality, VideoQuality
from tidal_dl.model import Album, Track, Video, Artist, Playlist, StreamUrl, VideoStreamUrl, SearchResult, Lyrics, Mix
import tidal_dl.apiKey as apiKey

__VERSION__ = '1.9.1'
__URL_PRE__ = 'https://api.tidalhifi.com/v1/'
__AUTH_URL__ = 'https://auth.tidal.com/v1/oauth2'
__API_KEY__ = {'clientId': '7m7Ap0JC9j1cOM3n',
               'clientSecret': 'vRAdA108tlvkJpTsGZS8rGZ7xTlbJ0qaZ2K9saEzsgY='}

# SSL Warnings
urllib3.disable_warnings()
# add retry number
requests.adapters.DEFAULT_RETRIES = 5


class LoginKey(object):
    def __init__(self):
        self.deviceCode = None
        self.userCode = None
        self.verificationUrl = None
        self.authCheckTimeout = None
        self.authCheckInterval = None
        self.userId = None
        self.countryCode = None
        self.accessToken = None
        self.refreshToken = None
        self.expiresIn = None


class __StreamRespond__(object):
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
        self.apiKey = __API_KEY__
        self.key = LoginKey()
        self.__debugVar = 0

    def __toJson__(self, string: str):
        try:
            json_object = json.loads(string)
        except:
            return None
        return json_object

    def __get__(self, path, params={}, retry=3, urlpre=__URL_PRE__):
        # deprecate the sessionId
        # header = {'X-Tidal-SessionId': self.key.sessionId}T
        header = {}
        if not isNull(self.key.accessToken):
            header = {'authorization': 'Bearer {}'.format(self.key.accessToken)}
        params['countryCode'] = self.key.countryCode

        result = None
        respond = None
        for index in range(0, retry):
            try:
                respond = requests.get(urlpre + path, headers=header, params=params)
                result = self.__toJson__(respond.text)
                break
            except:
                continue

        if result is None:
            return "Get operation err!" + respond.text, None
        if 'status' in result:
            if 'userMessage' in result and result['userMessage'] is not None:
                return result['userMessage'], None
            else:
                logging.error("[Get operation err] path=" + path + ". respon=" + respond.text)
                return "Get operation err!", None
        return None, result

    def __getItems__(self, path, params={}, retry=3):
        params['limit'] = 50
        params['offset'] = 0
        total = 0
        ret = []
        while True:
            msg, data = self.__get__(path, params, retry)
            if msg is not None:
                return msg, None
            
            if 'totalNumberOfItems'in data:
                total = data['totalNumberOfItems']
            if total > 0 and total <= len(ret):
                return None, ret
            
            num = 0
            for item in data["items"]:
                num += 1
                ret.append(item)
            if num < 50:
                break
            params['offset'] += num
        return None, ret

    def __getQualityString__(self, quality: AudioQuality):
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
        # array = txt.split("#EXT-X-STREAM-INF")
        array = txt.split("#")
        for item in array:
            if "RESOLUTION=" not in item:
                continue
            if "EXT-X-STREAM-INF:" not in item:
                continue
            stream = VideoStreamUrl()
            stream.codec = stringHelper.getSub(item, "CODECS=\"", "\"")
            stream.m3u8Url = "http" + stringHelper.getSubOnlyStart(item, "http").strip()
            stream.resolution = stringHelper.getSub(item, "RESOLUTION=", "http").strip()
            stream.resolution = stream.resolution.split(',')[0]
            stream.resolutions = stream.resolution.split("x")
            ret.append(stream)
        return ret

    def __post__(self, url, data, auth=None):
        retry = 3
        while retry > 0:
            try:
                result = requests.post(url, data=data, auth=auth, verify=False).json()
            except (
                    requests.ConnectionError,
                    requests.exceptions.ReadTimeout,
                    requests.exceptions.Timeout,
                    requests.exceptions.ConnectTimeout,
            ) as e:
                retry -= 1
                if retry <= 0:
                    return e, None
                continue
            return None, result

    def getDeviceCode(self):
        data = {
            'client_id': self.apiKey['clientId'],
            'scope': 'r_usr+w_usr+w_sub'
        }
        e, result = self.__post__(__AUTH_URL__ + '/device_authorization', data)
        if e is not None:
            return str(e), False

        if 'status' in result and result['status'] != 200:
            return "Device authorization failed. Please try again.", False

        self.key.deviceCode = result['deviceCode']
        self.key.userCode = result['userCode']
        self.key.verificationUrl = result['verificationUri']
        self.key.authCheckTimeout = result['expiresIn']
        self.key.authCheckInterval = result['interval']
        return None, True

    def checkAuthStatus(self):
        data = {
            'client_id': self.apiKey['clientId'],
            'device_code': self.key.deviceCode,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'scope': 'r_usr+w_usr+w_sub'
        }
        e, result = self.__post__(__AUTH_URL__ + '/token', data, (self.apiKey['clientId'], self.apiKey['clientSecret']))
        if e is not None:
            return str(e), False

        if 'status' in result and result['status'] != 200:
            if result['status'] == 400 and result['sub_status'] == 1002:
                return "pending", False
            else:
                return "Error while checking for authorization. Trying again...", False

        # if auth is successful:
        self.key.userId = result['user']['userId']
        self.key.countryCode = result['user']['countryCode']
        self.key.accessToken = result['access_token']
        self.key.refreshToken = result['refresh_token']
        self.key.expiresIn = result['expires_in']
        return None, True

    def verifyAccessToken(self, accessToken):
        header = {'authorization': 'Bearer {}'.format(accessToken)}
        result = requests.get('https://api.tidal.com/v1/sessions', headers=header).json()
        if 'status' in result and result['status'] != 200:
            return "Login failed!", False
        return None, True

    def refreshAccessToken(self, refreshToken):
        data = {
            'client_id': self.apiKey['clientId'],
            'refresh_token': refreshToken,
            'grant_type': 'refresh_token',
            'scope': 'r_usr+w_usr+w_sub'
        }

        e, result = self.__post__(__AUTH_URL__ + '/token', data, (self.apiKey['clientId'], self.apiKey['clientSecret']))
        if e is not None:
            return str(e), False

        # result = requests.post(__AUTH_URL__ + '/token', data=data, auth=(self.apiKey['clientId'], self.apiKey['clientSecret'])).json()
        if 'status' in result and result['status'] != 200:
            return "Refresh failed. Please log in again.", False

        # if auth is successful:
        self.key.userId = result['user']['userId']
        self.key.countryCode = result['user']['countryCode']
        self.key.accessToken = result['access_token']
        self.key.expiresIn = result['expires_in']
        return None, True

    def loginByAccessToken(self, accessToken, userid=None):
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
    
    def getMix(self, id):
        msg, tracks, videos = self.getItems(id, Type.Mix)
        if msg is not None:
            return msg, None
        mix = Mix()
        mix.id = id
        mix.tracks = tracks
        mix.videos = videos
        return None, mix
        
    def search(self, text: str, type: Type, offset: int, limit: int):
        typeStr = "ARTISTS,ALBUMS,TRACKS,VIDEOS,PLAYLISTS"
        if type == Type.Album:
            typeStr = "ALBUMS"
        if type == Type.Artist:
            typeStr = "ARTISTS"
        if type == Type.Track:
            typeStr = "TRACKS"
        if type == Type.Video:
            typeStr = "VIDEOS"
        if type == Type.Playlist:
            typeStr = "PLAYLISTS"

        params = {"query": text,
                  "offset": offset,
                  "limit": limit,
                  "types": typeStr}

        msg, data = self.__get__('search', params=params)
        return msg, dictToModel(data, SearchResult())

    def getLyrics(self, id):
        msg, data = self.__get__('tracks/' + str(id) + "/lyrics", urlpre='https://listen.tidal.com/v1/')
        return msg, dictToModel(data, Lyrics())

    def getItems(self, id, type: Type):
        if type == Type.Playlist:
            msg, data = self.__getItems__('playlists/' + str(id) + "/items")
        elif type == Type.Album:
            msg, data = self.__getItems__('albums/' + str(id) + "/items")
        elif type == Type.Mix:
            msg, data = self.__getItems__('mixes/' + str(id) + '/items')
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

    def getArtistAlbums(self, id, includeEP=False):
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
        resp = dictToModel(data, __StreamRespond__())

        if "vnd.tidal.bt" in resp.manifestMimeType:
            manifest = json.loads(base64.b64decode(resp.manifest).decode('utf-8'))
            ret = StreamUrl()
            ret.trackid = resp.trackid
            ret.soundQuality = resp.audioQuality
            ret.codec = manifest['codecs']
            ret.encryptionKey = manifest['keyId'] if 'keyId' in manifest else ""
            ret.url = manifest['urls'][0]
            return "", ret
        return "Can't get the streamUrl, type is " + resp.manifestMimeType, None

    def getVideoStreamUrl(self, id, quality: VideoQuality):
        paras = {"videoquality": "HIGH", "playbackmode": "STREAM", "assetpresentation": "FULL"}
        msg, data = self.__get__('videos/' + str(id) + "/playbackinfopostpaywall", paras)
        if msg is not None:
            return msg, None
        resp = dictToModel(data, __StreamRespond__())

        if "vnd.tidal.emu" in resp.manifestMimeType:
            manifest = json.loads(base64.b64decode(resp.manifest).decode('utf-8'))
            array = self.__getResolutionList__(manifest['urls'][0])
            icmp = int(quality.value)
            index = 0
            for item in array:
                if icmp <= int(item.resolutions[1]):
                    break
                index += 1
            if index >= len(array):
                index = len(array) - 1
            return "", array[index]
        return "Can't get the streamUrl, type is " + resp.manifestMimeType, None

    def getTrackContributors(self, id):
        msg, data = self.__get__('tracks/' + str(id) + "/contributors")
        return msg, data

    def getCoverUrl(self, sid, width="320", height="320"):
        if sid is None or sid == "":
            return None
        return "https://resources.tidal.com/images/" + sid.replace("-", "/") + "/" + width + "x" + height + ".jpg"

    def getArtistsName(self, artists=[]):
        array = []
        for item in artists:
            array.append(item.name)
        return " / ".join(array)

    def getFlag(self, data, type: Type, short=True, separator=" / "):
        master = False
        atmos = False
        explicit = False
        if type == Type.Album or type == Type.Track:
            if data.audioQuality == "HI_RES":
                master = True
            if type == Type.Album and "DOLBY_ATMOS" in data.audioModes:
                atmos = True
            if data.explicit is True:
                explicit = True
        if type == Type.Video:
            if data.explicit is True:
                explicit = True
        if not master and not atmos and not explicit:
            return ""
        array = []
        if master:
            array.append("M" if short else "Master")
        if atmos:
            array.append("A" if short else "Dolby Atmos")
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
        if 'mix' in url:
            etype = Type.Mix

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
        if obj is None and (etype == Type.Null or etype == Type.Mix):
            msg, obj = self.getMix(sid)

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
        if obj.__class__ == Mix:
            etype = Type.Mix
        return msg, etype, obj

    """
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
    """
