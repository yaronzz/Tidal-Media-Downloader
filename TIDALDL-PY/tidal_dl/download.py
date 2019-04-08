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

from aigpy import pathHelper
from aigpy import netHelper
from aigpy import fileHelper

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
        self.ffmpeg   = FFmpegTool()
        self.progress = ProgressTool(100)
        self.check    = CheckTool()

        pathHelper.mkdirs(self.config.outputdir + "/Album/")
        pathHelper.mkdirs(self.config.outputdir + "/Track/")
        pathHelper.mkdirs(self.config.outputdir + "/Playlist/")
        pathHelper.mkdirs(self.config.outputdir + "/Video/")

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
        if 'redownload' in paraList:
            redownload = paraList['redownload']
        if 'retry' in paraList:
            count = count + paraList['retry']
        if 'show' in paraList:
            printRet = paraList['show']

        if redownload == False:
            needDl = self.__isNeedDownload(paraList['path'], paraList['url'])
        
        if needDl:
            try:
                while count > 0:
                    count = count - 1
                    check = netHelper.downloadFile(paraList['url'], paraList['path'])
                    if check == True:
                        if paraList['key'] == '':
                            break
                        key,nonce = decrypt_security_token(paraList['key'])
                        decrypt_file(paraList['path'],key,nonce)
                        break
                if check:
                    self.tool.setTrackMetadata(paraList['trackinfo'], paraList['path'])
                    pstr = paraList['title']
                    bIsSuccess = True
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
        targetDir = self.config.outputdir + "/Album/" + title
        pathHelper.mkdirs(targetDir)
        # creat volumes dir
        count = 0
        numOfVolumes = int(albumInfo['numberOfVolumes'])
        if numOfVolumes > 1:
            while count < numOfVolumes:
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
        if extension == None:
            extension = ".m4a"

        numOfVolumes = int(albumInfo['numberOfVolumes'])
        if numOfVolumes <= 1:
            filePath = targetDir + "/" + pathHelper.replaceLimitChar(item['title'],'-') + extension
        else:
            index = item['volumeNumber']
            filePath = targetDir + "/Volume" + str(index-1) + "/" + pathHelper.replaceLimitChar(item['title'], '-') + extension
        return filePath

    def __getExistFiles(self, paths):
        ret = []
        for item in paths:
            if os.path.isfile(item):
                ret.append(item)
        return ret


    def downloadAlbum(self):
        while True:
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
                return
            # Creat OutputDir
            targetDir = self.__creatAlbumDir(aAlbumInfo)
            # write msg
            string = self.tool.convertAlbumInfoToString(aAlbumInfo, aAlbumTracks)
            with open(targetDir + "/AlbumInfo.txt", 'w', encoding='utf-8') as fd:
                fd.write(string)
            # download cover
            coverPath = targetDir + '/' + pathHelper.replaceLimitChar(aAlbumInfo['title'], '-') + '.jpg'
            coverUrl  = self.tool.getAlbumArtworkUrl(aAlbumInfo['cover'])
            netHelper.downloadFile(coverUrl, coverPath)
            # check exist files
            redownload = True
            existFiles = pathHelper.getDirFiles(targetDir)
            for item in existFiles:
                if '.txt' in item:
                    continue
                if '.jpg' in item:
                    continue
                check = printChoice("Some TrackFile Exist.Is Redownload?(y/n):")
                if check != 'y' and check != 'yes':
                    redownload = False
                break
            # download album tracks
            for item in aAlbumTracks['items']:
                streamInfo = self.tool.getStreamUrl(str(item['id']), self.config.quality)
                if self.tool.errmsg != "":
                    printErr(14,item['title'] + "(Get Stream Url Err!" + self.tool.errmsg + ")")
                    continue

                fileType = self._getSongExtension(streamInfo['url'])
                filePath = self.__getAlbumSongSavePath(targetDir, aAlbumInfo, item, fileType)
                paraList = {'redownload': redownload, 'title': item['title'], 'trackinfo': item, 'url': streamInfo['url'], 'path': filePath, 'retry': 3, 'key': streamInfo['encryptionKey']}
                self.thread.start(self.__thradfunc_dl, paraList)
            # wait all download thread
            self.thread.waitAll()
        return

    def downloadTrack(self):
        while True:
            targetDir = self.config.outputdir + "/Track/"
            print("----------------TRACK------------------")
            sID = printChoice("Enter TrackID(Enter '0' go back):", True, 0)
            if sID == 0:
                return

            aTrackInfo = self.tool.getTrack(sID)
            if self.tool.errmsg != "":
                printErr(0,"Get TrackInfo Err! " + self.tool.errmsg)
                return

            print("[TrackTitle ]       %s" % (aTrackInfo['title']))
            print("[Duration   ]       %s" % (aTrackInfo['duration']))
            print("[TrackNumber]       %s" % (aTrackInfo['trackNumber']))
            print("[Version    ]       %s\n" % (aTrackInfo['version']))
            # download
            streamInfo = self.tool.getStreamUrl(sID, self.config.quality)
            if self.tool.errmsg != "":
                printErr(14, aTrackInfo['title'] + "(Get Stream Url Err!" + self.tool.errmsg + ")")
                continue

            fileType = self._getSongExtension(streamInfo['url'])
            filePath = targetDir + "/" + pathHelper.replaceLimitChar(aTrackInfo['title'],'-') + fileType
            paraList = {'title': aTrackInfo['title'], 'trackinfo':aTrackInfo, 'url': streamInfo['url'], 'path': filePath, 'retry': 3, 'key':streamInfo['encryptionKey']}
            self.thread.start(self.__thradfunc_dl, paraList)
            # wait all download thread
            self.thread.waitAll()
        return

    def downloadVideo(self):
        while True:
            targetDir = self.config.outputdir + "/Video/"
            print("----------------VIDEO------------------")
            sID = printChoice("Enter VideoID(Enter '0' go back):", True, 0)
            if sID == 0:
                return
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
            print("-Index--Resolution--")
            for item in resolutionList:
                print('   ' + str(index) + "    " + resolutionList[index])
                index = index + 1
            print("--------------------")
            while True:
                index = printChoice("Enter ResolutionIndex:", True, 0)
                if index == '' or index == None or int(index) >= len(resolutionList):
                    printErr(0, "ResolutionIndex is err")
                    continue
                break

            path = targetDir + "/" + pathHelper.replaceLimitChar(aVideoInfo['title'],'-')+ ".mp4"
            path = os.path.abspath(path)
            if os.access(path, 0):
                os.remove(path)

            if self.ffmpeg.mergerByM3u8_Multithreading(urlList[int(index)], path, True):
                printSUCCESS(14, aVideoInfo['title'])
            else:
                printErr(14, aVideoInfo['title'])
        return

    def downloadPlaylist(self):
        while True:
            targetDir = self.config.outputdir + "/Playlist/"
            print("--------------PLAYLIST-----------------")
            sID = printChoice("Enter PlayListID(Enter '0' go back):")
            if sID == '0':
                return

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
            pathHelper.mkdirs(targetDir)
            # write msg
            string = self.tool.convertPlaylistInfoToString(aPlaylistInfo, aItemInfo)
            with open(targetDir + "/PlaylistInfo.txt", 'w', encoding = 'utf-8') as fd:
                fd.write(string)

            # download track
            bBreakFlag = False
            bFirstTime = True
            errIndex   = []
            index      = 0

            while bBreakFlag == False:
                self.check.clear()
                for item in aItemInfo:
                    type  = item['type']
                    item  = item['item']
                    if type != 'track':
                        continue

                    index = index + 1
                    if bFirstTime == False:
                        if self.check.isInErr(index - 1, errIndex) == False:
                            continue

                    streamInfo = self.tool.getStreamUrl(str(item['id']), self.config.quality)
                    if self.tool.errmsg != "":
                        printErr(14, item['title'] + "(Get Stream Url Err!!" + self.tool.errmsg + ")")
                        continue

                    fileType = self._getSongExtension(streamInfo['url'])
                    filePath = targetDir + '/' + pathHelper.replaceLimitChar(item['title'], '-') + fileType
                    paraList = {'title': item['title'], 'trackinfo':item, 'url': streamInfo['url'], 'path': filePath, 'retry': 3, 'key':streamInfo['encryptionKey']}
                    self.check.addPath(filePath)
                    if not os.path.isfile(filePath):
                        self.thread.start(self.__thradfunc_dl, paraList)
                self.thread.waitAll()
            
                bBreakFlag = True
                bFirstTime = False
            
                # check
                isErr, errIndex = self.check.checkPaths()
                if isErr:
                    check = printChoice("[Err]\t\t" + len(errIndex) + " Tracks Download Failed.Try Again?(y/n):")
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
                if self.ffmpeg.mergerByM3u8_Multithreading(urlList[0], filePath, showprogress=False):
                    printSUCCESS(14, item['title'])
                else:
                    printErr(14, item['title'])
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
            paraList = {'title': item['title'], 'trackinfo':item, 'url': streamInfo['url'], 'path': filePath, 'retry': 3, 'key':streamInfo['encryptionKey']}
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
            if self.ffmpeg.mergerByM3u8_Multithreading(urlList[0], filePath, showprogress=False):
                printSUCCESS(14, item['title'])
            else:
                printErr(14, item['title'])
        return






