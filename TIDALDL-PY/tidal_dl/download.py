#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   download.py
@Time    :   2019/02/27
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   Download Function
'''
import sys
import os
import codecs
from datetime import datetime
from aigpy import pathHelper
# from tidal_dl import netHelper
from aigpy import netHelper
from aigpy import fileHelper
from aigpy import cmdHelper

# from tidal_dl.ffmpegHelper import FFmpegTool
from aigpy.ffmpegHelper import FFmpegTool
from aigpy.cmdHelper import myinput,myinputInt
from aigpy.threadHelper import ThreadTool
from aigpy.progressHelper import ProgressTool

from tidal_dl.check import CheckTool
from tidal_dl.tidal import TidalTool
from tidal_dl.tidal import TidalConfig
from tidal_dl.tidal import TidalAccount
from tidal_dl.decryption import decrypt_security_token
from tidal_dl.decryption import decrypt_file
from tidal_dl.printhelper import printChoice, printErr, printSUCCESS

class Download(object):
    def __init__(self, threadNum=3):
        self.config   = TidalConfig()
        self.tool     = TidalTool()
        self.thread   = ThreadTool(int(threadNum))
        self.ffmpeg   = FFmpegTool(mergerTimeout=45)
        self.progress = ProgressTool(100)
        self.check    = CheckTool()

        self.showpro = False
        if self.config.showprogress == 'True':
            self.showpro = True

        pathHelper.mkdirs(self.config.outputdir + "/Album/")
        pathHelper.mkdirs(self.config.outputdir + "/Playlist/")
        pathHelper.mkdirs(self.config.outputdir + "/Video/")
        pathHelper.mkdirs(self.config.outputdir + "/Favorite/")

    def __isNeedDownload(self, path, url):
        curSize = fileHelper.getFileSize(path)
        if curSize <= 0:
            return True
        netSize = netHelper.getFileSize(url)
        if curSize >= netSize:
            return False
        return True

    # dowmload track thread
    def __thradfunc_dl(self, paraList):
        count      = 1
        printRet   = True
        pstr       = paraList['title'] + "(Download Err!)"
        redownload = True
        needDl     = True
        bIsSuccess = False
        albumInfo  = None
        index      = None
        coverpath  = None

        if 'redownload' in paraList:
            redownload = paraList['redownload']
        if 'retry' in paraList:
            count = count + paraList['retry']
        if 'show' in paraList:
            printRet = paraList['show']
        if 'album' in paraList:
            albumInfo = paraList['album']
        if 'index' in paraList:
            index = paraList['index']
        if 'coverpath' in paraList:
            coverpath = paraList['coverpath']

        if redownload is False:
            needDl = self.__isNeedDownload(paraList['path'], paraList['url'])

        # DEBUG
        # self.tool.setTrackMetadata(paraList['trackinfo'], paraList['path'], albumInfo, index, coverpath)
        showprogress = False
        if int(self.config.threadnum) <= 1 and self.showpro:
            showprogress = True

        Contributors = self.tool.getTrackContributors(paraList['trackinfo']['id'])
        if needDl:
            try:
                while count > 0:
                    count = count - 1
                    check = netHelper.downloadFile(paraList['url'], paraList['path'], showprogress=showprogress)
                    if check is True:
                        if paraList['key'] == '':
                            break
                        key,nonce = decrypt_security_token(paraList['key'])
                        decrypt_file(paraList['path'],key,nonce)
                        break
                if check:
                    bIsSuccess = True
                    paraList['path'] = self.tool.covertMp4toM4a(paraList['path'])
                    self.tool.setTrackMetadata(paraList['trackinfo'], paraList['path'], albumInfo, index, coverpath, Contributors)
                    pstr = paraList['title']
            except:
                pass
        else:
            pstr = paraList['title']
            bIsSuccess = True

        if printRet:
            if(bIsSuccess):
                printSUCCESS(14, pstr)
            else:
                printErr(14, pstr)
        return

    # creat album output dir
    def __creatAlbumDir(self, albumInfo):
        # creat outputdir
        title = pathHelper.replaceLimitChar(albumInfo['title'], '-')
        author = pathHelper.replaceLimitChar(albumInfo['artist']['name'], '-')
        if self.config.addyear == 'True':
            title = '[' + str(datetime.strptime(albumInfo['releaseDate'], '%Y-%m-%d').year) + '] '+title
        targetDir = self.config.outputdir + "/Album/" + author + '/' + title
        # targetDir = self.config.outputdir + "/Album/" + title + '(' + author + ')'
        targetDir = os.path.abspath(targetDir)
        pathHelper.mkdirs(targetDir)
        # creat volumes dir
        count = 1
        numOfVolumes = int(albumInfo['numberOfVolumes'])
        if numOfVolumes > 1:
            while count < numOfVolumes + 1:
                volumeDir = targetDir + "/Volume" + str(count)
                pathHelper.mkdirs(volumeDir)
                count = count + 1
        return targetDir
    
    def _getSongExtension(self, downloadUrl):
        if downloadUrl.find('.flac?') != -1:
            return '.flac'
        if downloadUrl.find('.m4a?') != -1:
            return '.m4a'
        if downloadUrl.find('.mp4?') != -1:
            return '.mp4'
        return '.m4a'

    def __getAlbumSongSavePath(self, targetDir, albumInfo, item, extension):
        if extension is None:
            extension = ".m4a"
        
        seq  = self.tool.getIndexStr(item['trackNumber'], albumInfo['numberOfTracks'])
        name = seq + pathHelper.replaceLimitChar(item['title'], '-')
        if self.config.addhyphen == 'True':
            name = seq + '- ' + pathHelper.replaceLimitChar(item['title'], '-')

        seq  = item['volumeNumber']
        path = targetDir + "/"
        if int(albumInfo['numberOfVolumes']) > 1:
            path += 'Volume' + str(seq) + "/"
        
        filePath = path + name + extension
        return filePath

    def __getExistFiles(self, paths):
        ret = []
        for item in paths:
            if os.path.isfile(item):
                ret.append(item)
        return ret

    def __getVideoResolutionIndex(self, reslist):
        array = []
        for item in reslist:
            subs = item.split('x')
            subs = subs[1].split(',')
            array.append(int(subs[0]))
        cmp = int(self.config.resolution)
        ret = 0
        for item in array:
            if cmp >= item:
                return ret
            ret += 1
        return len(array) - 1

    def downloadAlbum(self, album_id=None, redl_flag=None):
        while_count = 9999
        while while_count > 0:
            while_count -= 1

            if album_id is not None:
                while_count = 0
                sID = album_id
            else:
                print("----------------ALBUM------------------")
                sID = printChoice("Enter AlbumID(Enter '0' go back):", True, 0)
                if sID == 0:
                    return

            aAlbumInfo = self.tool.getAlbum(sID)
            if self.tool.errmsg != "":
                printErr(0, "Get AlbumInfo Err! " + self.tool.errmsg)
                continue

            print("[Title]       %s" % (aAlbumInfo['title']))
            print("[SongNum]     %s\n" % (aAlbumInfo['numberOfTracks']))

            # Get Tracks
            aAlbumTracks = self.tool.getAlbumTracks(sID)
            if self.tool.errmsg != "":
                printErr(0,"Get AlbumTracks Err!" + self.tool.errmsg)
                continue
            aAlbumVideos = self.tool.getAlbumVideos(sID)
            
            # Creat OutputDir
            targetDir = self.__creatAlbumDir(aAlbumInfo)
            # write msg
            string = self.tool.convertAlbumInfoToString(aAlbumInfo, aAlbumTracks)
            with codecs.open(targetDir + "/AlbumInfo.txt", 'w', 'utf-8') as fd:
                fd.write(string)
            # download cover
            coverPath = targetDir + '/' + pathHelper.replaceLimitChar(aAlbumInfo['title'], '-') + '.jpg'
            coverUrl  = self.tool.getAlbumArtworkUrl(aAlbumInfo['cover'])
            netHelper.downloadFile(coverUrl, coverPath)
            # check exist files
            redownload = True
            if redl_flag is None:
                existFiles = pathHelper.getDirFiles(targetDir)
                for item in existFiles:
                    if '.txt' in item:
                        continue
                    if '.jpg' in item:
                        continue
                    check = printChoice("Some trackFile exist.Is redownload?(y/n):")
                    if not cmdHelper.isInputYes(check):
                        redownload = False
                    break
            else:
                redownload = redl_flag

            # download album tracks
            for item in aAlbumTracks['items']:
                streamInfo = self.tool.getStreamUrl(str(item['id']), self.config.quality)
                if self.tool.errmsg != "":
                    printErr(14,item['title'] + "(Get Stream Url Err!" + self.tool.errmsg + ")")
                    continue

                fileType = self._getSongExtension(streamInfo['url'])
                filePath = self.__getAlbumSongSavePath(targetDir, aAlbumInfo, item, fileType)
                paraList = {'album': aAlbumInfo, 
                            'redownload': redownload, 
                            'title': item['title'], 
                            'trackinfo': item, 
                            'url': streamInfo['url'], 
                            'path': filePath, 
                            'retry': 3, 
                            'key': streamInfo['encryptionKey'], 
                            'coverpath': coverPath}
                self.thread.start(self.__thradfunc_dl, paraList)
            # wait all download thread
            self.thread.waitAll()
            self.tool.removeTmpFile(targetDir)

            # download video
            
            for item in aAlbumVideos:
                item = item['item']
                filePath = targetDir + '/' + pathHelper.replaceLimitChar(item['title'], '-') + ".mp4"
                filePath = os.path.abspath(filePath)
                if os.access(filePath, 0):
                    os.remove(filePath)

                resolutionList, urlList = self.tool.getVideoResolutionList(item['id'])
                selectIndex = self.__getVideoResolutionIndex(resolutionList)
                if self.ffmpeg.mergerByM3u8_Multithreading2(urlList[int(selectIndex)], filePath, showprogress=self.showpro):
                    printSUCCESS(14, item['title'])
                else:
                    printErr(14, item['title'])
            return

        return

    def downloadArtistAlbum(self):
        while True:
            print("-------------ARTIST ALBUM--------------")
            sID = printChoice("Enter ArtistID(Enter '0' go back):", True, 0)
            if sID == 0:
                return

            array = self.tool.getArtistAlbum(sID)
            if self.tool.errmsg != "":
                printErr(0, "Get AlbumList Err! " + self.tool.errmsg)
                continue
            
            redownload = True
            check = printChoice("Skip downloaded files?(y/n):")
            if not cmdHelper.isInputYes(check):
                redownload = False

            for index, item in enumerate(array):
                print("----Album[{0}/{1}]----".format(index+1, len(array)))
                self.downloadAlbum(item['id'], redownload)

    def downloadTrack(self, track_id=None):
        while_count = 9999
        while while_count > 0:
            while_count -= 1

            if track_id is not None:
                while_count = 0
                sID = track_id
            else:
                print("----------------TRACK------------------")
                sID = printChoice("Enter TrackID(Enter '0' go back):", True, 0)
                if sID == 0:
                    return
            aTrackInfo = self.tool.getTrack(sID)
            if self.tool.errmsg != "":
                printErr(0,"Get TrackInfo Err! " + self.tool.errmsg)
                return
            aAlbumInfo = self.tool.getAlbum(aTrackInfo['album']['id'])
            if self.tool.errmsg != "":
                printErr(0,"Get TrackInfo Err! " + self.tool.errmsg)
                return
            
            # t = self.tool.getTrackContributors(sID)

            print("[AlbumTitle ]       %s" % (aAlbumInfo['title']))
            print("[TrackTitle ]       %s" % (aTrackInfo['title']))
            print("[Duration   ]       %s" % (aTrackInfo['duration']))
            print("[TrackNumber]       %s" % (aTrackInfo['trackNumber']))
            print("[Version    ]       %s\n" % (aTrackInfo['version']))

            # Creat OutputDir
            targetDir = self.__creatAlbumDir(aAlbumInfo)
            # download cover
            coverPath = targetDir + '/' + pathHelper.replaceLimitChar(aAlbumInfo['title'], '-') + '.jpg'
            coverUrl  = self.tool.getAlbumArtworkUrl(aAlbumInfo['cover'])
            netHelper.downloadFile(coverUrl, coverPath)

            # download
            streamInfo = self.tool.getStreamUrl(sID, self.config.quality)
            if self.tool.errmsg != "":
                printErr(14, aTrackInfo['title'] + "(Get Stream Url Err!" + self.tool.errmsg + ")")
                continue

            fileType = self._getSongExtension(streamInfo['url'])
            filePath = self.__getAlbumSongSavePath(targetDir, aAlbumInfo, aTrackInfo, fileType)
            # filePath = targetDir + "/" + pathHelper.replaceLimitChar(aTrackInfo['title'],'-') + fileType
            paraList = {'album':aAlbumInfo, 
                        'title': aTrackInfo['title'], 
                        'trackinfo':aTrackInfo, 
                        'url': streamInfo['url'], 
                        'path': filePath, 
                        'retry': 3, 
                        'key':streamInfo['encryptionKey'],
                        'coverpath': coverPath}
            self.thread.start(self.__thradfunc_dl, paraList)
            # wait all download thread
            self.thread.waitAll()
            self.tool.removeTmpFile(targetDir)
        return

    def downloadVideo(self, video_id = None):
        flag = True
        while flag:
            targetDir = self.config.outputdir + "/Video/"
            if video_id is None:
                print("----------------VIDEO------------------")
                sID = printChoice("Enter VideoID(Enter '0' go back):", True, 0)
                if sID == 0:
                    return
            else:
                flag = False
                sID = video_id

            aVideoInfo = self.tool.getVideo(sID)
            if self.tool.errmsg != "":
                printErr(0,"Get VideoInfo Err! " + self.tool.errmsg)
                continue

            print("[Title      ]       %s" % (aVideoInfo['title']))
            print("[Duration   ]       %s" % (aVideoInfo['duration']))
            print("[TrackNumber]       %s" % (aVideoInfo['trackNumber']))
            print("[Type       ]       %s\n" % (aVideoInfo['type']))

            # get resolution
            index = 0
            resolutionList, urlList = self.tool.getVideoResolutionList(sID)
            if self.tool.errmsg != "":
                printErr(14, self.tool.errmsg)
                continue

            index=self.__getVideoResolutionIndex(resolutionList)
            path = targetDir + "/" + pathHelper.replaceLimitChar(aVideoInfo['title'],'-')+ ".mp4"
            path = os.path.abspath(path)
            if os.access(path, 0):
                os.remove(path)

            if self.ffmpeg.mergerByM3u8_Multithreading2(urlList[int(index)], path, True):
                printSUCCESS(14, aVideoInfo['title'])
            else:
                printErr(14, aVideoInfo['title'])
        return

    def downloadPlaylist(self, playlist_id=None):
        while True:
            targetDir = self.config.outputdir + "/Playlist/"
            if playlist_id is None:
                print("--------------PLAYLIST-----------------")
                sID = printChoice("Enter PlayListID(Enter '0' go back):")
                if sID == '0':
                    return
            else: sID=playlist_id

            aPlaylistInfo,aItemInfo = self.tool.getPlaylist(sID)
            if self.tool.errmsg != "":
                printErr(0,"Get PlaylistInfo Err! " + self.tool.errmsg)
                return

            print("[Title]                %s" % (aPlaylistInfo['title']))
            print("[Type]                 %s" % (aPlaylistInfo['type']))
            print("[NumberOfTracks]       %s" % (aPlaylistInfo['numberOfTracks']))
            print("[NumberOfVideos]       %s" % (aPlaylistInfo['numberOfVideos']))
            print("[Duration]             %s\n" % (aPlaylistInfo['duration']))

            # Creat OutputDir
            targetDir = targetDir + pathHelper.replaceLimitChar(aPlaylistInfo['title'],'-')
            targetDir = os.path.abspath(targetDir)
            pathHelper.mkdirs(targetDir)
            # write msg
            string = self.tool.convertPlaylistInfoToString(aPlaylistInfo, aItemInfo)
            with codecs.open(targetDir + "/PlaylistInfo.txt", 'w','utf-8') as fd:
                fd.write(string)
            # download cover
            coverPath = targetDir + '/' + pathHelper.replaceLimitChar(aPlaylistInfo['title'], '-') + '.jpg'
            coverUrl  = self.tool.getPlaylistArtworkUrl(aPlaylistInfo['uuid'])
            check     = netHelper.downloadFile(coverUrl, coverPath)


            # download track
            bBreakFlag = False
            bFirstTime = True
            errIndex   = []
            index      = 0

            while bBreakFlag is False:
                self.check.clear()
                index = 0
                for item in aItemInfo:
                    type  = item['type']
                    item  = item['item']
                    if type != 'track':
                        continue
                    
                    index = index + 1
                    if bFirstTime is False:
                        if self.check.isInErr(index - 1, errIndex) == False:
                            continue

                    streamInfo = self.tool.getStreamUrl(str(item['id']), self.config.quality)
                    if self.tool.errmsg != "":
                        printErr(14, item['title'] + "(Get Stream Url Err!!" + self.tool.errmsg + ")")
                        continue

                    fileType = self._getSongExtension(streamInfo['url'])
                    filePath = targetDir + '/' + pathHelper.replaceLimitChar(item['title'], '-') + fileType
                    aAlbumInfo = self.tool.getAlbum(item['album']['id'])
                    coverPath = targetDir + '/' + pathHelper.replaceLimitChar(aAlbumInfo['title'], '-') + '.jpg'
                    coverUrl  = self.tool.getAlbumArtworkUrl(aAlbumInfo['cover'])
                    netHelper.downloadFile(coverUrl, coverPath)
                    paraList = {'album': aAlbumInfo, 'index': index, 'title': item['title'], 'trackinfo': item, 'url': streamInfo['url'], 'path': filePath, 'retry': 3, 'key': streamInfo['encryptionKey'], 'coverpath': coverPath}
                    self.check.addPath(filePath)
                    # if not os.path.isfile(filePath):
                    self.thread.start(self.__thradfunc_dl, paraList)
                self.thread.waitAll()
                self.tool.removeTmpFile(targetDir)
                
                bBreakFlag = True
                bFirstTime = False
            
                # check
                isErr, errIndex = self.check.checkPaths()
                if isErr:
                    check = printChoice("[Err]\t\t" + str(len(errIndex)) + " Tracks Download Failed.Try Again?(y/n):")
                    if check == 'y' or check == 'Y':
                        bBreakFlag = False

            # download video 
            for item in aItemInfo:
                type = item['type']
                item = item['item']
                if type != 'video':
                    continue
                
                filePath = targetDir + '/' + pathHelper.replaceLimitChar(item['title'], '-') + ".mp4"
                filePath = os.path.abspath(filePath)
                if os.access(filePath, 0):
                    os.remove(filePath)

                videoID = item['id']
                resolutionList, urlList = self.tool.getVideoResolutionList(videoID)
                if urlList is None:
                    printErr(14, item['title'] + '(' + self.tool.errmsg + ')')
                else:
                    selectIndex=self.__getVideoResolutionIndex(resolutionList)
                    if self.ffmpeg.mergerByM3u8_Multithreading2(urlList[int(selectIndex)], filePath, showprogress=self.showpro):
                        printSUCCESS(14, item['title'])
                    else:
                        printErr(14, item['title'] + "(Download Or Merger Err!)")
            if playlist_id is not None: return
        return

    def downloadFavorite(self):
        targetDir = self.config.outputdir + "/Favorite/"
        pathHelper.mkdirs(targetDir)
        
        trackList,videoList = self.tool.getFavorite(self.config.userid)
        if self.tool.errmsg != "":
            printErr(0, "Get FavoriteList Err! " + self.tool.errmsg)
            return
        
        print("[NumberOfTracks]       %s" % (len(trackList)))
        print("[NumberOfVideos]       %s" % (len(videoList)))
        # download track
        for item in trackList:
            item = item['item']
            streamInfo = self.tool.getStreamUrl(str(item['id']), self.config.quality)
            if self.tool.errmsg != "":
                printErr(14, item['title'] + "(Get Stream Url Err!!" + self.tool.errmsg + ")")
                continue
            
            fileType = self._getSongExtension(streamInfo['url'])
            filePath = targetDir + '/' + pathHelper.replaceLimitChar(item['title'], '-') + fileType
            aAlbumInfo = self.tool.getAlbum(item['album']['id'])
            paraList = {'album': aAlbumInfo, 'title': item['title'], 'trackinfo': item, 'url': streamInfo['url'], 'path': filePath, 'retry': 3, 'key': streamInfo['encryptionKey']}
            self.thread.start(self.__thradfunc_dl, paraList)
        self.thread.waitAll()

        # download video
        for item in videoList:
            item = item['item']

            filePath = targetDir + '/' + pathHelper.replaceLimitChar(item['title'], '-') + ".mp4"
            filePath = os.path.abspath(filePath)
            if os.access(filePath, 0):
                os.remove(filePath)

            resolutionList, urlList = self.tool.getVideoResolutionList(item['id'])
            selectIndex = self.__getVideoResolutionIndex(resolutionList)
            if self.ffmpeg.mergerByM3u8_Multithreading2(urlList[int(selectIndex)], filePath, showprogress=self.showpro):
                printSUCCESS(14, item['title'])
            else:
                printErr(14, item['title'])
        return

    def downloadUrl(self, link):
        stype,sid=self.tool.parseLink(link)
        if stype is None or sid is None:
            return
        if stype == "album":
            print("----------------ALBUM------------------")
            self.downloadAlbum(sid)
        elif stype == "track":
            print("----------------TRACK------------------")
            self.downloadTrack(sid)
        elif stype == "video":
            print("----------------VIDEO------------------")
            self.downloadVideo(sid)
        elif stype == "playlist":
            print("--------------PLAYLIST-----------------")
            self.downloadPlaylist(sid)
    
    def downloadByFile(self, path):
        if not os.path.exists(path):
            return
        arr = self.tool.parseFile(path)
        print("----------------FILE------------------")
        print("[NumOfAlbum]       %s" % (len(arr['album'])))
        print("[NumOfTrack]       %s" % (len(arr['track'])))
        print("[NumOfVideo]       %s" % (len(arr['video'])))
        print("[NumOfUrl]         %s" % (len(arr['url'])))
        
        if len(arr['album']) > 0:
            redownload = True
            check = printChoice("Skip downloaded files?(y/n):")
            if not cmdHelper.isInputYes(check):
                redownload = False

        for index, item in enumerate(arr['album']):
            print("----Album[{0}/{1}]----".format(index+1, len(arr['album'])))
            print("[ID]          %s" % (item))
            self.downloadAlbum(item, redownload)
        for index, item in enumerate(arr['track']):
            print("----Track[{0}/{1}]----".format(index+1, len(arr['track'])))
            print("[ID]                %s" % (item))
            self.downloadTrack(item)
        for index, item in enumerate(arr['video']):
            print("----Video[{0}/{1}]----".format(index+1, len(arr['video'])))
            print("[ID]                %s" % (item))
            self.downloadVideo(item)
        for index, item in enumerate(arr['url']):
            print("----Url[{0}/{1}]----".format(index+1, len(arr['url'])))
            print("[link]        %s" % (item))
            stype, sid = self.tool.parseLink(item)
            if stype is None or sid is None:
                printErr(14,'Link can`t parse!')
                continue
            print("[ID]          %s" % (sid))
            if stype == "album":
                print("[Type]        %s" % ("album"))
                self.downloadAlbum(sid)
            if stype == "track":
                print("[Type]        %s" % ("track"))
                self.downloadTrack(sid)
            if stype == "video":
                print("[Type]        %s" % ("video"))
                self.downloadVideo(sid)
