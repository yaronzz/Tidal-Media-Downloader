import sys
import os

from aigpy import pathHelper
from aigpy import netHelper

from aigpy.ffmpegHelper import FFmpegTool
from aigpy.cmdHelper import myinput
from aigpy.threadHelper import ThreadTool

from tidal_dl.tidal import TidalTool
from tidal_dl.tidal import TidalConfig
from tidal_dl.tidal import TidalAccount

class Download(object):
    def __init__(self, threadNum=50):
        self.config = TidalConfig()
        self.tool   = TidalTool()
        self.thread = ThreadTool(threadNum)
        self.ffmpeg = FFmpegTool()

        pathHelper.mkdirs(self.config.outputdir + "\\Album\\")
        pathHelper.mkdirs(self.config.outputdir + "\\Track\\")
        pathHelper.mkdirs(self.config.outputdir + "\\Playlist\\")
        pathHelper.mkdirs(self.config.outputdir + "\\Video\\")

    # dowmload track thread
    def __thradfunc_dl(self, paraList):
        count    = 1
        printRet = True
        pstr     = '{:<14}'.format("[ERR]") + paraList['title'] + "(Download Err!)"
        if 'retry' in paraList:
            count = count + paraList['retry']
        if 'show' in paraList:
            printRet = paraList['show']

        try:
            while count > 0:
                count = count - 1
                check = netHelper.downloadFile(paraList['url'], paraList['path'])
                if check == True:
                    break
            if check:
                pstr = '{:<14}'.format("[SUCCESS]") + paraList['title']
        except:
            pass
        
        if printRet:
            print(pstr)
        return

    # creat album output dir
    def __creatAlbumDir(self, albumInfo):
        # creat outputdir
        title = pathHelper.replaceLimitChar(albumInfo['title'], '-')
        targetDir = self.config.outputdir + "\\Album\\" + title
        pathHelper.mkdirs(targetDir)
        # creat volumes dir
        count = 0
        numOfVolumes = int(albumInfo['numberOfVolumes'])
        if numOfVolumes > 1:
            while count < numOfVolumes:
                volumeDir = targetDir + "\\Volume" + str(count)
                pathHelper.mkdirs(volumeDir)
                count = count + 1
        return targetDir
    
    def __getAlbumSongSavePath(self, targetDir, albumInfo, item):
        numOfVolumes = int(albumInfo['numberOfVolumes'])
        if numOfVolumes <= 1:
            filePath = targetDir + "\\" + pathHelper.replaceLimitChar(item['title'],'-') + ".m4a"
        else:
            index = item['volumeNumber']
            filePath = targetDir + "\\Volume" + index + pathHelper.replaceLimitChar(item['title'], '-') + ".m4a"
        return filePath

    def downloadAlbum(self):
        while True:
            print("----------------ALBUM------------------")
            sID = myinput("Enter AlbumID（Enter '0' go back）:")
            if sID == '0':
                return

            aAlbumInfo = self.tool.getAlbum(sID)
            if self.tool.errmsg != "":
                print("Get AlbumInfo Err!")
                continue

            print("[Title]       %s" % (aAlbumInfo['title']))
            print("[SongNum]     %s\n" % (aAlbumInfo['numberOfTracks']))

            # Get Tracks
            aAlbumTracks = self.tool.getAlbumTracks(sID)
            if self.tool.errmsg != "":
                print("Get AlbumTracks Err!")
                return
            # Creat OutputDir
            targetDir = self.__creatAlbumDir(aAlbumInfo)
            # write msg
            string = self.tool.convertAlbumInfoToString(aAlbumInfo, aAlbumTracks)
            with open(targetDir + "\\AlbumInfo.txt", 'w') as fd:
                fd.write(string)
            # download album tracks
            for item in aAlbumTracks['items']:
                filePath = self.__getAlbumSongSavePath(targetDir, aAlbumInfo, item)
                streamInfo = self.tool.getStreamUrl(str(item['id']), self.config.quality)
                if self.tool.errmsg != "":
                    print("[Err]\t\t" + item['title'] + "(Get Stream Url Err!)")
                    continue

                paraList = {'title': item['title'], 'url': streamInfo['url'], 'path': filePath, 'retry': 3}
                self.thread.start(self.__thradfunc_dl, paraList)
            # wait all download thread
            self.thread.waitAll()
        return

    def downloadTrack(self):
        while True:
            targetDir = self.config.outputdir + "\\Track\\"
            print("----------------TRACK------------------")
            sID = myinput("Enter TrackID（Enter '0' go back）:")
            if sID == '0':
                return

            aTrackInfo = self.tool.getTrack(sID)
            if self.tool.errmsg != "":
                print("Get TrackInfo Err!")
                return

            print("[TrackTitle ]       %s" % (aTrackInfo['title']))
            print("[Duration   ]       %s" % (aTrackInfo['duration']))
            print("[TrackNumber]       %s" % (aTrackInfo['trackNumber']))
            print("[Version    ]       %s\n" % (aTrackInfo['version']))
            # download
            filePath = targetDir + "\\" + pathHelper.replaceLimitChar(aTrackInfo['title'],'-') + ".m4a"
            streamInfo = self.tool.getStreamUrl(sID, self.config.quality)
            if self.tool.errmsg != "":
                print("[Err]\t\t" + aTrackInfo['title'] + "(Get Stream Url Err!)")
                continue
            paraList = {'title': aTrackInfo['title'], 'url': streamInfo['url'], 'path': filePath, 'retry': 3}
            self.thread.start(self.__thradfunc_dl, paraList)
            # wait all download thread
            self.thread.waitAll()
        return

    def downloadVideo(self):
        while True:
            targetDir = self.config.outputdir + "\\Video\\"
            print("----------------VIDEO------------------")
            sID = myinput("Enter VideoID（Enter '0' go back）:")
            if sID == '0':
                return
            aVideoInfo = self.tool.getVideo(sID)
            if self.tool.errmsg != "":
                print("Get VideoInfo Err!")
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
                index = myinput("Enter ResolutionIndex:")
                if index == '' or index == None or int(index) >= len(resolutionList):
                    print("[Err] " + "ResolutionIndex is err")
                    continue
                break

            path = targetDir + "\\" + pathHelper.replaceLimitChar(aVideoInfo['title'],'-')+ ".mp4"
            path = os.path.abspath(path)
            if os.access(path, 0):
                os.remove(path)

            if self.ffmpeg.mergerByM3u8_Multithreading(urlList[int(index)], path):
                print('{:<14}'.format("[SUCCESS]") + aVideoInfo['title'])
            else:
                print('{:<14}'.format("[ERR]") + aVideoInfo['title'])
        return

    def downloadPlaylist(self):
        while True:
            targetDir = self.config.outputdir + "\\Playlist\\"
            print("--------------PLAYLIST-----------------")
            sID = myinput("Enter PlayListID（Enter '0' go back）:")
            if sID == '0':
                return

            aPlaylistInfo,aItemInfo = self.tool.getPlaylist(sID)
            if self.tool.errmsg != "":
                print("Get PlaylistInfo Err!")
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
            with open(targetDir + "\\PlaylistInfo.txt", 'w') as fd:
                fd.write(string)
            # download track
            for item in aItemInfo['items']:
                type = item['type']
                item = item['item']
                if type != 'track':
                    continue

                filePath = targetDir + '\\' + pathHelper.replaceLimitChar(item['title'], '-') + ".m4a";
                streamInfo = self.tool.getStreamUrl(str(item['id']), self.config.quality)
                if self.tool.errmsg != "":
                    print("[Err]\t\t" + item['title'] + "(Get Stream Url Err!)")
                    continue

                paraList = {'title': item['title'], 'url': streamInfo['url'], 'path': filePath, 'retry': 3}
                self.thread.start(self.__thradfunc_dl, paraList)
            self.thread.waitAll()

            # download video 
            for item in aItemInfo['items']:
                type = item['type']
                item = item['item']
                if type != 'video':
                    continue
                
                filePath = targetDir + '\\' + pathHelper.replaceLimitChar(item['title'], '-') + ".mp4"
                filePath = os.path.abspath(filePath)
                if os.access(filePath, 0):
                    os.remove(filePath)

                resolutionList, urlList = self.tool.getVideoResolutionList(sID)
                if self.ffmpeg.mergerByM3u8_Multithreading(urlList[0], filePath):
                    print('{:<14}'.format("[SUCCESS]") + item['title'])
                else:
                    print('{:<14}'.format("[ERR]") + item['title'])
        return

def downloadByFile():
    return


