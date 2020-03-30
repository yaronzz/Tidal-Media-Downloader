#!/usr/bin/env python
# coding=utf-8
# -*- encoding: utf-8 -*-
'''
@File    :   tidal.py
@Time    :   2019/02/27
@Author  :   Yaron Huang
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   Tidal API
'''
import os
import re
import uuid
import requests
import json

from aigpy import fileHelper
from aigpy import pathHelper
from aigpy import configHelper
from aigpy import netHelper
from aigpy import systemHelper
from aigpy import tagHelper
from aigpy import configHelper
from aigpy.ffmpegHelper import FFmpegTool
# from tidal_dl import tagHelper
from pydub import AudioSegment
from tidal_dl.printhelper import printWarning

VERSION = '1.9.1'
URL_PRE = 'https://api.tidalhifi.com/v1/'
QUALITY = ['HI_RES', 'LOSSLESS', 'HIGH', 'LOW']
TYPE_ARR = ['album', 'track', 'video', 'playlist', 'artist']
RESOLUTION = ['1080', '720', '480', '360', '240']


class TidalTool(object):
    def __init__(self):
        self.config = TidalConfig()
        self.errmsg = ""
        self.tmpfileFlag = 'TIDAL_TMP_'
        self.ffmpeg = FFmpegTool(1)

    def _get(self, url, params={}):
        retry = 3
        sessionid = self.config.sessionid
        if 'soundQuality' in params: 
            if params['soundQuality'] == 'LOSSLESS':
                sessionid = self.config.sessionid2

        while retry > 0:
            retry -= 1
            try:
                self.errmsg = ""
                params['countryCode'] = self.config.countrycode
                resp = requests.get(
                    URL_PRE + url,
                    headers={'X-Tidal-SessionId': sessionid},
                    params=params).json()
                if 'status' in resp and resp['status'] == 404 and resp['subStatus'] == 2001:
                    self.errmsg = '{}. This might be region-locked.'.format(resp['userMessage'])
                elif 'status' in resp and resp['status'] == 401 and resp['subStatus'] == 4005: #'Asset is not ready for playback'
                    sessionid = self.config.sessionid2
                    continue
                elif 'status' in resp and not resp['status'] == 200:
                    self.errmsg = '{}. Get operation err!'.format(resp['userMessage'])
                    # self.errmsg = "Get operation err!"
                return resp
            except Exception as e:
                if retry <= 0:
                    self.errmsg = 'Function `Http-Get` Err! ' + str(e)
                    return None

    def setTag(self, tag, srcfile, coverpath=None):
        path = pathHelper.getDirName(srcfile)
        name = pathHelper.getFileNameWithoutExtension(srcfile)
        ext = pathHelper.getFileExtension(srcfile)
        oext = ext

        if 'm4a' in ext or 'mp4' in ext:
            oext = '.mp3'
        if 'mp3' not in oext:
            coverpath = None
        tmpfile = path + '/' + 'TMP' + name + oext

        try:
            data = AudioSegment.from_file(srcfile, format=ext[1:])
            check = data.export(tmpfile, format=oext[1:], tags=tag, cover=coverpath)
            check.close()
        except Exception as e:
            pathHelper.remove(tmpfile)
            return

        if fileHelper.getFileSize(tmpfile) > 0:
            pathHelper.remove(srcfile)
            os.rename(tmpfile, path + '/' + name + oext)
        else:
            pathHelper.remove(tmpfile)

    def setTrackMetadata_old(self, track_info, file_path, album_info, index, coverpath):
        tag = {'Artist': track_info['artist']['name'],
               'Album': track_info['album']['title'],
               'Title': track_info['title'],
               'CopyRight': track_info['copyright'],
               'Track': track_info['trackNumber']}
        if index is not None:
            tag['Track'] = str(index)
        if album_info is not None:
            tag['Date'] = album_info['releaseDate']
            tag['Year'] = album_info['releaseDate'].split('-')[0]
        self.setTag(tag, file_path, coverpath)
        return

    def covertMp4toM4a(self, file_path):
        if self.config.onlym4a != "True":
            return file_path
        if '.mp4' not in file_path:
            return file_path
        if not self.ffmpeg.enable:
            return file_path
        new_path = file_path.replace('.mp4', '.m4a')

        pathHelper.remove(new_path)
        if self.ffmpeg.covertFile(file_path, new_path):
            pathHelper.remove(file_path)
            return new_path
        else:
            return file_path

    def _parseContributors(self, roleType, Contributors):
        if Contributors is None:
            return None
        try:
            ret = []
            for item in Contributors['items']:
                if item['role'] == roleType:
                    ret.append(item['name'])
            return ret
        except:
            return None

    def setTrackMetadata(self, track_info, file_path, album_info, index, coverpath, Contributors):
        # isrc,replayGain,releasedate
        obj = tagHelper.TagTool(file_path)
        obj.album = track_info['album']['title']
        obj.title = track_info['title']
        obj.artist = self._getArtists(track_info['artists'])
        obj.copyright = track_info['copyright']
        obj.tracknumber = track_info['trackNumber']
        obj.discnumber = track_info['volumeNumber']
        obj.isrc = track_info['isrc']
        obj.composer = self._parseContributors('Composer', Contributors)
        if index is not None:
            obj.tracknumber = str(index)
        if album_info is not None:
            obj.albumartist = self._getArtists(album_info['artists'])
            obj.date = album_info['releaseDate']
            obj.totaldisc = album_info['numberOfVolumes']
            if obj.totaldisc <= 1:
                obj.totaltrack = album_info['numberOfTracks']
        obj.save(coverpath)
        return

    def removeTmpFile(self, path):
        for root, dirs, files in os.walk(path):
            for name in files:
                if self.tmpfileFlag in name:
                    pathHelper.remove(os.path.join(root, name))

    def getStreamUrl(self, track_id, quality):
        url = self._get('tracks/' + str(track_id) + '/streamUrl', {'soundQuality': quality})
        if not url:
            resp = self._get('tracks/{}/playbackinfopostpaywall'.format(track_id), {
                 'audioquality': quality,
                 'playbackmode': 'STREAM',
                 'assetpresentation': 'FULL'})
            if resp and 'trackId' in resp:
                #  printWarning(14, "Redirecting: {} -> {}".format(track_id, resp['trackId']))
                track_id = resp['trackId']
                url = self._get('tracks/' + str(track_id) + '/streamUrl', {'soundQuality': quality})
        return url

    def _getArtists(self, pHash):
        ret = []
        for item in pHash:
            ret.append(item['name'])
        return ret

    def getIndexStr(self, index, sum):
        pre = "0"
        if sum > 99:
            pre = "00"
        if index < 10:
            return pre+str(index) + " "
        if index < 99 and sum > 99:
            return "0"+str(index) + " "
        return str(index) + " "

    def _fixSameTrackName(self, tracks, isOnLayer2=False):
        same = {}
        for item in tracks:
            if isOnLayer2:
                item = item['item']
            if 'version' in item:
                if item['version'] is not None:
                    item['title'] = item['title'] + ' - ' + item['version']
            if item['title'] in same:
                same[item['title']] += 1
            else:
                same[item['title']] = 1
        for item in same:
            if same[item] <= 1:
                continue
            index = 1
            for track in tracks:
                if track:
                    track = track['item']
                if track['title'] != item:
                    continue
                track['title'] += str(index)
                index += 1
        return tracks

    def getPlaylist(self, playlist_id):
        info = self._get('playlists/' + playlist_id)
        if self.errmsg != "":
            return None, None
        list = self.__getItemsList('playlists/' + playlist_id + '/items')
        list = self._fixSameTrackName(list, True)
        return info, list

    def getAlbumTracks(self, album_id):
        info = self._get('albums/' + str(album_id) + '/tracks')
        if self.errmsg != "":
            return info
        # sum = info['totalNumberOfItems']
        for item in info['items']:
            if 'version' in item and item['version'] is not None:
                item['title'] += ' - ' + item['version']
        #     indexs = self._getIndexStr(item['trackNumber'],sum)
        #     item['title'] = indexs + " " + item['title']
        # info['items'] = self._fixSameTrackName(info['items'])
        return info

    def getAlbumVideos(self, album_id):
        # info = self._get('albums/' + str(album_id) + '/items')
        info = self.__getItemsList('albums/' + str(album_id) + '/items')
        if self.errmsg != "":
            return []
        ret = []
        for item in info:
            if item['type'] == 'video':
                ret.append(item)
        return ret

    def getTrack(self, track_id):
        item = self._get('tracks/' + str(track_id))
        if 'version' in item and item['version'] is not None:
            item['title'] += ' - ' + item['version']
        return item

    def getAlbum(self, album_id):
        return self._get('albums/' + str(album_id))

    def getVideo(self, video_id):
        return self._get('videos/' + str(video_id))

    def getFavorite(self, user_id):
        trackList = self.__getItemsList('users/' + str(user_id) + '/favorites/tracks')
        videoList = self.__getItemsList('users/' + str(user_id) + '/favorites/videos')
        return trackList, videoList

    def getArtistAlbum(self, artist_id, includeSingles): 
        if includeSingles: 
            items1 = self.__getItemsList('artists/' + str(artist_id) + '/albums',{'filter': 'EPSANDSINGLES'}) 
        else: 
            items1 = []
        # items2 = self.__getItemsList('artists/' + str(artist_id) + '/albums',{'filter': 'COMPILATIONS'})
        items3 = self.__getItemsList('artists/' + str(artist_id) + '/albums')
        itemall = items1 + items3
        return itemall

    def __getItemsList(self, url, in_dirs={}):
        in_dirs['limit'] = 0
        ret = self._get(url, in_dirs)
        count = ret['totalNumberOfItems']
        offset = 0
        limit = 100
        retList = []
        while offset < count:
            in_dirs['limit'] = limit
            in_dirs['offset'] = offset
            items = self._get(url, in_dirs)
            if self.errmsg != "":
                if self.errmsg.find('Too big page') >= 0:
                    limit = limit - 10
                    continue
                else:
                    return retList
            offset = offset + limit
            if retList == None:
                retList = items['items']
            else:
                retList.extend(items['items'])
        return retList

    def getTrackContributors(self, track_id):
        return self._get('tracks/' + str(track_id) + '/contributors')

    def getAlbumArtworkUrl(self, coverid, size=1280):
        if coverid is not None: 
            return 'https://resources.tidal.com/images/{0}/{1}x{1}.jpg'.format(coverid.replace('-', '/'), size) 
        else: 
            return '' 

    def getPlaylistArtworkUrl(self, playlist_uuid, size=1280):
        return 'http://images.tidalhifi.com/im/im?w={1}&h={2}&uuid={0}&rows=2&cols=3&noph'.format(playlist_uuid, size, size)

    def getVideoResolutionList(self, video_id):
        info = self._get('videos/' + str(video_id) + '/streamurl')
        if self.errmsg != "":
            return None, None
        content = netHelper.downloadString(info['url'], None)
        resolutionList, urlList = self.__parseVideoMasterAll(str(content))
        return resolutionList, urlList

    def getVideoMediaPlaylist(self, url):
        urlList = self.__parseVideoMediaPlaylist(url)
        return urlList

    def searchTrack(self, query):
        ret = self._get('search/tracks', {'query': query, 'offset': 0, 'limit': 99})
        return ret

    def __parseVideoMasterAll(self, content):
        pattern = re.compile(r"(?<=RESOLUTION=).+?(?=\\n)")
        resolutionList = pattern.findall(content)
        pattern = re.compile(r"(?<=http).+?(?=\\n)")
        pList = pattern.findall(content)
        urlList = []
        for item in pList:
            urlList.append("http"+item)

        return resolutionList, urlList

    def __parseVideoMediaPlaylist(self, url):
        content = netHelper.downloadString(url, None)
        pattern = re.compile(r"(?<=http).+?(?=\\n)")
        plist = pattern.findall(str(content))
        urllist = []
        for item in plist:
            urllist.append("http"+item)
        return urllist

    def convertAlbumInfoToString(self, aAlbumInfo, aAlbumTracks):
        str = ""
        str += "[ID]          %d\n" % (aAlbumInfo['id'])
        str += "[Title]       %s\n" % (aAlbumInfo['title'])
        str += "[Artists]     %s\n" % (aAlbumInfo['artist']['name'])
        str += "[ReleaseDate] %s\n" % (aAlbumInfo['releaseDate'])
        str += "[SongNum]     %s\n" % (aAlbumInfo['numberOfTracks'])
        str += "[Duration]    %s\n" % (aAlbumInfo['duration'])
        str += '\n'

        i = 0
        while True:
            if i >= int(aAlbumInfo['numberOfVolumes']):
                break
            i = i + 1
            str += "===========Volume %d=============\n" % i
            for item in aAlbumTracks['items']:
                if item['volumeNumber'] != i:
                    continue
                str += '{:<8}'.format("[%d]" % item['trackNumber'])
                str += "%s\n" % item['title']
        return str

    def convertPlaylistInfoToString(seld, aPlaylistInfo, aTrackItems):
        str = ""
        str += "[Title]           %s\n" % (aPlaylistInfo['title'])
        str += "[Type]            %s\n" % (aPlaylistInfo['type'])
        str += "[NumberOfTracks]  %s\n" % (aPlaylistInfo['numberOfTracks'])
        str += "[NumberOfVideos]  %s\n" % (aPlaylistInfo['numberOfVideos'])
        str += "[Duration]        %s\n" % (aPlaylistInfo['duration'])

        i = 0
        str += "===========Track=============\n"
        for item in aTrackItems:
            type = item['type']
            item = item['item']
            if type != 'track':
                continue

            i = i + 1
            str += '{:<8}'.format("[%d]" % i) + item['title'] + '\n'

        i = 0
        str += "\n===========Video=============\n"
        for item in aTrackItems:
            type = item['type']
            item = item['item']
            if type != 'video':
                continue

            i = i + 1
            str += '{:<8}'.format("[%d]" % i) + item['title'] + '\n'
        return str

    def parseLink(self,  link):
        link = link.strip()
        if link.find('http') < 0:
            return None, None

        urlpres = ['tidal.com/', 'tidal.com/browse/']
        for pre in urlpres:
            stype = re.findall(pre + "(.+?)/", link)
            if len(stype) <= 0 or stype[0] not in TYPE_ARR:
                continue
            sid = re.findall(pre+stype[0]+"/(.+)/", link)
            if len(sid) <= 0:
                sid = re.findall(pre+stype[0]+"/(.+)", link)
            if len(sid) <= 0:
                return None, None
            return stype[0], sid[0]
        return None, None

    def parseFile(self, path):
        cfp = configHelper.ParseNoEqual(path)
        ret = cfp
        if 'album' not in ret:
            ret['album'] = []
        if 'artist' not in ret: 
            ret['artist'] = [] 
        if 'track' not in ret:
            ret['track'] = []
        if 'video' not in ret:
            ret['video'] = []
        if 'url' not in ret:
            ret['url'] = []
        return ret

# LogIn and Get SessionID


class TidalAccount(object):
    def __init__(self, username, password, bymobile=False):
        token = 'u5qPNNYIbD0S0o36MrAiFZ56K6qMCrCmYPzZuTnV'
        if bymobile == True:
            token = 'kgsOOmYk3zShYrNP'

        self.username = username
        self.token = token
        self.uuid = str(uuid.uuid4()).replace('-', '')[16:]
        self.errmsg = ""
        self.getSessionID(password)

    def getSessionID(self, password):
        postParams = {
            'username': self.username,
            'password': password,
            'token': self.token,
            'clientUniqueKey': self.uuid,
            'clientVersion': VERSION,
        }
        re = requests.post(URL_PRE + 'login/username', data=postParams).json()
        if 'status' in re:
            if re['status'] == 401:
                self.errmsg = "Username or password err!"
            else:
                self.errmsg = "Get sessionid err!"
        else:
            self.session_id = re['sessionId']
            self.user_id = re['userId']
            self.country_code = re['countryCode']

            re = requests.get(URL_PRE + 'users/' + str(self.user_id), params={'sessionId': self.session_id}).json()
            if 'status' in re and not re['status'] == 200:
                self.errmsg = "Sessionid is unvalid!"

# Config Tool


class TidalConfig(object):
    FILE_NAME = "tidal-dl.ini"

    def __init__(self):
        self.outputdir = configHelper.GetValue("base", "outputdir", "./", self.FILE_NAME)
        self.sessionid = configHelper.GetValue("base", "sessionid", "", self.FILE_NAME)
        self.countrycode = configHelper.GetValue("base", "countrycode", "", self.FILE_NAME)
        self.quality = configHelper.GetValue("base", "quality", "LOSSLESS", self.FILE_NAME)
        self.resolution = configHelper.GetValue("base", "resolution", "720", self.FILE_NAME)
        self.username = configHelper.GetValue("base", "username", "", self.FILE_NAME)
        self.password = configHelper.GetValue("base", "password", "", self.FILE_NAME)
        self.userid = configHelper.GetValue("base", "userid", "", self.FILE_NAME)
        self.threadnum = configHelper.GetValue("base", "threadnum", "1", self.FILE_NAME)
        self.sessionid2 = configHelper.GetValue("base", "sessionid2", "", self.FILE_NAME)
        self.onlym4a = configHelper.GetValue("base", "onlym4a", "False", self.FILE_NAME)
        self.showprogress = configHelper.GetValue("base", "showprogress", "False", self.FILE_NAME)
        self.addhyphen = configHelper.GetValue("base", "addhyphen", "False", self.FILE_NAME)
        self.addyear = configHelper.GetValue("base", "addyear", "No", self.FILE_NAME)
        self.plfile2arfolder = configHelper.GetValue("base", "plfile2arfolder", "False", self.FILE_NAME)
        self.addexplicit = configHelper.GetValue("base", "addexplicit", "False", self.FILE_NAME)
        self.includesingle = configHelper.GetValue("base", "includesingle", "True", self.FILE_NAME)
        self.savephoto = configHelper.GetValue("base", "savephoto", "True", self.FILE_NAME)

    def set_savephoto(self, status):
        if status == 0:
            self.savephoto = "False"
        else:
            self.savephoto = "True"
        configHelper.SetValue("base", "savephoto", self.savephoto, self.FILE_NAME)

    def set_includesingle(self, status):
        if status == 0:
            self.includesingle = "False"
        else:
            self.includesingle = "True"
        configHelper.SetValue("base", "includesingle", self.includesingle, self.FILE_NAME)

    def set_plfile2arfolder(self, status):
        if status == 0:
            self.plfile2arfolder = "False"
        else:
            self.plfile2arfolder = "True"
        configHelper.SetValue("base", "plfile2arfolder", self.plfile2arfolder, self.FILE_NAME)

    def set_onlym4a(self, status):
        if status == 0:
            self.onlym4a = "False"
        else:
            self.onlym4a = "True"
        configHelper.SetValue("base", "onlym4a", self.onlym4a, self.FILE_NAME)

    def set_showprogress(self, status):
        if status == 0:
            self.showprogress = "False"
        else:
            self.showprogress = "True"
        configHelper.SetValue("base", "showprogress", self.showprogress, self.FILE_NAME)

    def set_addhyphen(self, status):
        if status == 0:
            self.addhyphen = "False"
        else:
            self.addhyphen = "True"
        configHelper.SetValue("base", "addhyphen", self.addhyphen, self.FILE_NAME)

    def set_addyear(self, status):
        self.addyear = status
        configHelper.SetValue("base", "addyear", status, self.FILE_NAME)

    def set_addexplicit(self, status):
        if status == 0:
            self.addexplicit = "False"
        else:
            self.addexplicit = "True"
        configHelper.SetValue("base", "addexplicit", self.addexplicit, self.FILE_NAME)

    def set_threadnum(self, threadnum):
        self.threadnum = threadnum
        configHelper.SetValue("base", "threadnum", threadnum, self.FILE_NAME)

    def set_outputdir(self, outputdir):
        self.outputdir = outputdir
        configHelper.SetValue("base", "outputdir", outputdir, self.FILE_NAME)

    def set_quality(self, quality):
        self.quality = quality
        configHelper.SetValue("base", "quality", quality, self.FILE_NAME)

    def set_resolution(self, resolution):
        self.resolution = resolution
        configHelper.SetValue("base", "resolution", resolution, self.FILE_NAME)

    def set_account(self, username, password, sessionid, countrycode, userid, sessionid2):
        self.username = username
        self.password = password
        self.sessionid = sessionid
        self.sessionid2 = sessionid2
        self.countrycode = countrycode
        configHelper.SetValue("base", "username", username, self.FILE_NAME)
        configHelper.SetValue("base", "password", password, self.FILE_NAME)
        configHelper.SetValue("base", "sessionid", sessionid, self.FILE_NAME)
        configHelper.SetValue("base", "sessionid2", sessionid2, self.FILE_NAME)
        configHelper.SetValue("base", "countrycode", countrycode, self.FILE_NAME)
        configHelper.SetValue("base", "userid", str(userid), self.FILE_NAME)

    def valid_quality(self, quality):
        if quality in QUALITY:
            return True
        return False

    def valid_threadnum(self, threadnum):
        try:
            num = int(threadnum)
            return num > 0
        except:
            return False


# if __name__ == '__main__':
#     tool = TidalTool()
#     tool.getArtistAlbum('3529466')
