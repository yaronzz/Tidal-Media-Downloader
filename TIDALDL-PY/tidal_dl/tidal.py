#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tidal.py
@Time    :   2019/02/27
@Author  :   Yaronzz
@VERSION :   3.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   tidal api
'''
import base64
import hashlib
import random
import secrets
import time
from typing import List
from urllib.parse import parse_qs, urlencode, urlparse

from tidal_dl import dash

import requests

from model import *
from settings import *

# SSL Warnings | retry number
requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5


def _supports_pkce(api_key):
    value = api_key.get('supportsPkce')
    if isinstance(value, str):
        return value.lower() == 'true'
    return bool(value)


def _generate_code_verifier():
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')


def _generate_code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')


class TidalAPI(object):
    def __init__(self):
        self.key = LoginKey()
        self.apiKey = {'clientId': '7m7Ap0JC9j1cOM3n',
                       'clientSecret': 'vRAdA108tlvkJpTsGZS8rGZ7xTlbJ0qaZ2K9saEzsgY='}

    def __get__(self, path, params={}, urlpre='https://api.tidalhifi.com/v1/'):
        header = {}
        header = {'authorization': f'Bearer {self.key.accessToken}'}
        params['countryCode'] = self.key.countryCode
        errmsg = "Get operation err!"
        for index in range(0, 3):
            try:
                respond = requests.get(urlpre + path, headers=header, params=params)
                if respond.url.find("playbackinfopostpaywall") != -1 and SETTINGS.downloadDelay is not False:
                    # random sleep between 0.5 and 5 seconds and print it
                    sleep_time = random.randint(500, 5000) / 1000
                    print(
                        f"Sleeping for {sleep_time} seconds, to mimic human behaviour and prevent too many requests error")
                    time.sleep(sleep_time)

                if respond.status_code == 429:
                    print('Too many requests, waiting for 20 seconds...')
                    # Loop countdown 20 seconds and print the remaining time
                    for i in range(20, 0, -1):
                        time.sleep(1)
                        print(i, end=' ')
                    print('')
                    continue

                result = json.loads(respond.text)
                if 'status' not in result:
                    return result

                if 'userMessage' in result and result['userMessage'] is not None:
                    errmsg += result['userMessage']
                break
            except Exception as e:
                if index >= 3:
                    errmsg += respond.text

        raise Exception(errmsg)

    def __getItems__(self, path, params={}):
        params['limit'] = 50
        params['offset'] = 0
        total = 0
        ret = []
        while True:
            data = self.__get__(path, params)
            if 'totalNumberOfItems' in data:
                total = data['totalNumberOfItems']
            if total > 0 and total <= len(ret):
                return ret

            ret += data["items"]
            num = len(data["items"])
            if num < 50:
                break
            params['offset'] += num
        return ret

    def __getResolutionList__(self, url):
        ret = []
        txt = requests.get(url).content.decode('utf-8')
        # array = txt.split("#EXT-X-STREAM-INF")
        array = txt.split("#")
        for item in array:
            if "RESOLUTION=" not in item:
                continue
            if "EXT-X-STREAM-INF:" not in item:
                continue
            stream = VideoStreamUrl()
            stream.codec = aigpy.string.getSub(item, "CODECS=\"", "\"")
            stream.m3u8Url = "http" + aigpy.string.getSubOnlyStart(item, "http").strip()
            stream.resolution = aigpy.string.getSub(item, "RESOLUTION=", "http").strip()
            stream.resolution = stream.resolution.split(',')[0]
            stream.resolutions = stream.resolution.split("x")
            ret.append(stream)
        return ret

    def __post__(self, path, data, auth=None, urlpre='https://auth.tidal.com/v1/oauth2'):
        for index in range(3):
            try:
                result = requests.post(urlpre + path, data=data, auth=auth, verify=False).json()
                return result
            except Exception as e:
                if index == 2:
                    raise e

    def getDeviceCode(self) -> str:
        data = {
            'client_id': self.apiKey['clientId'],
            'scope': 'r_usr+w_usr+w_sub'
        }
        result = self.__post__('/device_authorization', data)
        if 'status' in result and result['status'] != 200:
            raise Exception("Device authorization failed. Please choose another apikey.")

        self.key.deviceCode = result['deviceCode']
        self.key.userCode = result['userCode']
        self.key.verificationUrl = result['verificationUri']
        self.key.authCheckTimeout = result['expiresIn']
        self.key.authCheckInterval = result['interval']
        return "http://" + self.key.verificationUrl + "/" + self.key.userCode

    def checkAuthStatus(self) -> bool:
        data = {
            'client_id': self.apiKey['clientId'],
            'device_code': self.key.deviceCode,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'scope': 'r_usr+w_usr+w_sub'
        }
        auth = (self.apiKey['clientId'], self.apiKey['clientSecret'])
        result = self.__post__('/token', data, auth)
        if 'status' in result and result['status'] != 200:
            if result['status'] == 400 and result['sub_status'] == 1002:
                return False
            else:
                raise Exception("Error while checking for authorization. Trying again...")

        # if auth is successful:
        self.key.userId = result['user']['userId']
        self.key.countryCode = result['user']['countryCode']
        self.key.accessToken = result['access_token']
        self.key.refreshToken = result['refresh_token']
        self.key.expiresIn = result['expires_in']
        return True

    def verifyAccessToken(self, accessToken) -> bool:
        header = {'authorization': 'Bearer {}'.format(accessToken)}
        result = requests.get('https://api.tidal.com/v1/sessions', headers=header).json()

        if 'status' in result and result['status'] != 200:
            return False
        return True

    def refreshAccessToken(self, refreshToken) -> bool:
        data = {
            'client_id': self.apiKey['clientId'],
            'refresh_token': refreshToken,
            'grant_type': 'refresh_token',
            'scope': 'r_usr+w_usr+w_sub'
        }
        auth = (self.apiKey['clientId'], self.apiKey['clientSecret'])
        result = self.__post__('/token', data, auth)
        if 'status' in result and result['status'] != 200:
            return False

        # if auth is successful:
        self.key.userId = result['user']['userId']
        self.key.countryCode = result['user']['countryCode']
        self.key.accessToken = result['access_token']
        self.key.expiresIn = result['expires_in']
        return True

    def startPkceAuthorization(self) -> str:
        if not _supports_pkce(self.apiKey):
            raise Exception("Current API key does not support PKCE login.")

        authorize_url = self.apiKey.get('pkceAuthorizeUrl', 'https://login.tidal.com/authorize')
        redirect_uri = self.apiKey.get('pkceRedirectUri', 'https://listen.tidal.com/callback')
        scope = self.apiKey.get('pkceScope', 'r_usr+w_usr+w_sub')

        verifier = _generate_code_verifier()
        self.key.pkceCodeVerifier = verifier
        self.key.pkceState = secrets.token_urlsafe(32)
        self.key.pkceRedirectUri = redirect_uri

        params = {
            'response_type': 'code',
            'client_id': self.apiKey['clientId'],
            'scope': scope,
            'redirect_uri': redirect_uri,
            'state': self.key.pkceState,
            'code_challenge': _generate_code_challenge(verifier),
            'code_challenge_method': 'S256'
        }
        return f"{authorize_url}?{urlencode(params)}"

    def completePkceAuthorization(self, redirect_url: str) -> bool:
        if not _supports_pkce(self.apiKey):
            raise Exception("Current API key does not support PKCE login.")
        if self.key.pkceCodeVerifier is None:
            raise Exception("PKCE authorization has not been initiated.")

        parsed = urlparse(redirect_url.strip())
        params = parse_qs(parsed.query)
        if 'code' not in params or len(params['code']) == 0:
            raise Exception("Authorization code not found in redirect URL.")

        state = params.get('state', [None])[0]
        if self.key.pkceState and state is not None and state != self.key.pkceState:
            raise Exception("Authorization state mismatch. Please restart the PKCE login flow.")

        code = params['code'][0]
        scope = self.apiKey.get('pkceScope', 'r_usr+w_usr+w_sub')

        data = {
            'grant_type': 'authorization_code',
            'client_id': self.apiKey['clientId'],
            'code_verifier': self.key.pkceCodeVerifier,
            'redirect_uri': self.key.pkceRedirectUri,
            'code': code,
            'scope': scope
        }

        result = self.__post__('/token', data, auth=None)
        if 'status' in result and result['status'] != 200:
            message = result.get('userMessage') or result.get('error_description') or 'PKCE authorization failed.'
            raise Exception(message)

        self.key.userId = result['user']['userId']
        self.key.countryCode = result['user']['countryCode']
        self.key.accessToken = result['access_token']
        self.key.refreshToken = result.get('refresh_token')
        self.key.expiresIn = result.get('expires_in')
        self.key.pkceState = None
        self.key.pkceCodeVerifier = None
        self.key.pkceRedirectUri = None
        return True

    def loginByAccessToken(self, accessToken, userid=None):
        header = {'authorization': 'Bearer {}'.format(accessToken)}
        result = requests.get('https://api.tidal.com/v1/sessions', headers=header).json()
        if 'status' in result and result['status'] != 200:
            raise Exception("Login failed!")

        if not aigpy.string.isNull(userid):
            if str(result['userId']) != str(userid):
                raise Exception("User mismatch! Please use your own accesstoken.", )

        self.key.userId = result['userId']
        self.key.countryCode = result['countryCode']
        self.key.accessToken = accessToken

        return

    def getAlbum(self, id) -> Album:
        return aigpy.model.dictToModel(self.__get__('albums/' + str(id)), Album())

    def getPlaylist(self, id) -> Playlist:
        return aigpy.model.dictToModel(self.__get__('playlists/' + str(id)), Playlist())
    
    def getPlaylistSelf(self) -> List[Playlist]:
        ret = self.__get__(f'users/{self.key.userId}/playlists')
        playlists = []
        for item in ret['items']:
            playlists.append(aigpy.model.dictToModel(item, Playlist()))
        return playlists

    def getArtist(self, id) -> Artist:
        return aigpy.model.dictToModel(self.__get__('artists/' + str(id)), Artist())

    def getTrack(self, id) -> Track:
        return aigpy.model.dictToModel(self.__get__('tracks/' + str(id)), Track())

    def getVideo(self, id) -> Video:
        return aigpy.model.dictToModel(self.__get__('videos/' + str(id)), Video())

    def getMix(self, id) -> Mix:
        mix = Mix()
        mix.id = id
        mix.tracks, mix.videos = self.getItems(id, Type.Mix)
        return None, mix

    def getTypeData(self, id, type: Type):
        if type == Type.Album:
            return self.getAlbum(id)
        if type == Type.Artist:
            return self.getArtist(id)
        if type == Type.Track:
            return self.getTrack(id)
        if type == Type.Video:
            return self.getVideo(id)
        if type == Type.Playlist:
            return self.getPlaylist(id)
        if type == Type.Mix:
            return self.getMix(id)
        return None

    def search(self, text: str, type: Type, offset: int = 0, limit: int = 10) -> SearchResult:
        typeStr = type.name.upper() + "S"

        if type == Type.Null:
            typeStr = "ARTISTS,ALBUMS,TRACKS,VIDEOS,PLAYLISTS"

        params = {"query": text,
                  "offset": offset,
                  "limit": limit,
                  "types": typeStr}
        return aigpy.model.dictToModel(self.__get__('search', params=params), SearchResult())

    def getSearchResultItems(self, result: SearchResult, type: Type):
        if type == Type.Track:
            return result.tracks.items
        if type == Type.Video:
            return result.videos.items
        if type == Type.Album:
            return result.albums.items
        if type == Type.Artist:
            return result.artists.items
        if type == Type.Playlist:
            return result.playlists.items
        return []

    def getLyrics(self, id) -> Lyrics:
        data = self.__get__(f'tracks/{str(id)}/lyrics', urlpre='https://listen.tidal.com/v1/')
        return aigpy.model.dictToModel(data, Lyrics())

    def getItems(self, id, type: Type):
        if type == Type.Playlist:
            data = self.__getItems__('playlists/' + str(id) + "/items")
        elif type == Type.Album:
            data = self.__getItems__('albums/' + str(id) + "/items")
        elif type == Type.Mix:
            data = self.__getItems__('mixes/' + str(id) + '/items')
        else:
            raise Exception("invalid Type!")

        tracks = []
        videos = []
        for item in data:
            if item['type'] == 'track' and item['item']['streamReady']:
                tracks.append(aigpy.model.dictToModel(item['item'], Track()))
            else:
                videos.append(aigpy.model.dictToModel(item['item'], Video()))
        return tracks, videos

    def getArtistAlbums(self, id, includeEP=False):
        data = self.__getItems__(f'artists/{str(id)}/albums')
        albums = list(aigpy.model.dictToModel(item, Album()) for item in data)
        if not includeEP:
            return albums

        data = self.__getItems__(f'artists/{str(id)}/albums', {"filter": "EPSANDSINGLES"})
        albums += list(aigpy.model.dictToModel(item, Album()) for item in data)
        return albums

    # from https://github.com/Dniel97/orpheusdl-tidal/blob/master/interface.py#L582
    def parse_mpd(self, xml: bytes) -> dash.Manifest:
        manifest = dash.parse_manifest(xml)

        for period in manifest.periods:
            for adaptation in period.adaptation_sets:
                if adaptation.content_type == 'audio':
                    for representation in adaptation.representations:
                        if representation.segments:
                            return manifest
        raise ValueError('No playable audio representations were found in MPD manifest.')

    def getStreamUrl(self, id, quality: AudioQuality):
        squality = "HI_RES"
        if quality == AudioQuality.Normal:
            squality = "LOW"
        elif quality == AudioQuality.High:
            squality = "HIGH"
        elif quality == AudioQuality.HiFi:
            squality = "LOSSLESS"
        elif quality == AudioQuality.Max:
            squality = "HI_RES_LOSSLESS"

        paras = {"audioquality": squality, "playbackmode": "STREAM", "assetpresentation": "FULL"}
        data = self.__get__(f'tracks/{str(id)}/playbackinfopostpaywall', paras)
        resp = aigpy.model.dictToModel(data, StreamRespond())

        if "vnd.tidal.bt" in resp.manifestMimeType:
            manifest = json.loads(base64.b64decode(resp.manifest).decode('utf-8'))
            ret = StreamUrl()
            ret.trackid = resp.trackid
            ret.soundQuality = resp.audioQuality
            ret.codec = manifest['codecs']
            ret.encryptionKey = manifest['keyId'] if 'keyId' in manifest else ""
            ret.url = manifest['urls'][0]
            ret.urls = [ret.url]
            return ret
        elif "dash+xml" in resp.manifestMimeType:
            xml_bytes = base64.b64decode(resp.manifest)
            manifest = self.parse_mpd(xml_bytes)
            ret = StreamUrl()
            ret.trackid = resp.trackid
            ret.soundQuality = resp.audioQuality
            audio_reps = []
            for period in manifest.periods:
                for adaptation in period.adaptation_sets:
                    if adaptation.content_type == 'audio':
                        audio_reps.extend(adaptation.representations)

            if not audio_reps:
                raise ValueError('MPD manifest did not contain any audio representations.')

            representation = next((rep for rep in audio_reps if rep.segments), audio_reps[0])

            codec = (representation.codec or '').upper()
            if codec.startswith('MP4A'):
                codec = 'AAC'
            ret.codec = codec
            ret.encryptionKey = ""  # manifest['keyId'] if 'keyId' in manifest else ""
            ret.urls = representation.segments
            if len(ret.urls) > 0:
                ret.url = ret.urls[0]
            return ret

        raise Exception("Can't get the streamUrl, type is " + resp.manifestMimeType)

    def getVideoStreamUrl(self, id, quality: VideoQuality):
        paras = {"videoquality": "HIGH", "playbackmode": "STREAM", "assetpresentation": "FULL"}
        data = self.__get__(f'videos/{str(id)}/playbackinfopostpaywall', paras)
        resp = aigpy.model.dictToModel(data, StreamRespond())

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
            return array[index]
        raise Exception("Can't get the streamUrl, type is " + resp.manifestMimeType)

    def getTrackContributors(self, id):
        return self.__get__(f'tracks/{str(id)}/contributors')

    def getCoverUrl(self, sid, width="320", height="320"):
        if sid is None:
            return ""
        return f"https://resources.tidal.com/images/{sid.replace('-', '/')}/{width}x{height}.jpg"

    def getCoverData(self, sid, width="320", height="320"):
        url = self.getCoverUrl(sid, width, height)
        try:
            return requests.get(url).content
        except:
            return ''

    def getArtistsName(self, artists=[]):
        array = list(item.name for item in artists)
        return ", ".join(array)

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
        if "tidal.com" not in url:
            return Type.Null, url

        url = url.lower()
        for index, item in enumerate(Type):
            if item.name.lower() in url:
                etype = item
                return etype, aigpy.string.getSub(url, etype.name.lower() + '/', '/')
        return Type.Null, url

    def getByString(self, string):
        if aigpy.string.isNull(string):
            raise Exception("Please enter something.")

        obj = None
        etype, sid = self.parseUrl(string)
        for index, item in enumerate(Type):
            if etype != Type.Null and etype != item:
                continue
            if item == Type.Null:
                continue
            try:
                obj = self.getTypeData(sid, item)
                return item, obj
            except:
                continue

        raise Exception("No result.")

# Singleton
TIDAL_API = TidalAPI()
