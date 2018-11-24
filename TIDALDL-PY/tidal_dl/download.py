import sys
import os
import subprocess

from ffmpeg import video

from aigpy import pathHelper
from aigpy import netHelper
from aigpy import threadHelper
from aigpy.cmdHelper import myinput

import tidal_dl.tidal as tidal
from tidal_dl.tidal import TidalConfig, TidalTool, TidalAccount


# dowmload track thread
def thradfunc_dltrack(paraList):
    try:
        count = 1
        if 'retry' in paraList:
            count = count + paraList['retry']

        while True:
            count = count - 1
            path  = pathHelper.replaceLimiChar(paraList['path'],'-')
            check = netHelper.downloadFile(paraList['url'], paraList['path'])
            if check == True:
                break
            if(count <= 0):
                break

        if check == False:
            print('{:<14}'.format("[Err]") + paraList['title'] + "(Download Err!)")
        else:
            print('{:<14}'.format("[SUCCESS]") + paraList['title'])
    except:
        print('{:<14}'.format("[Err]") + paraList['title'] + "(Download Err!)")

# Creat outputDir
def mkdirOutputDir(aAlbumInfo, aTrackInfo = None, aPlaylistInfo = None, aVideoInfo = None):
    cf = TidalConfig()
    if aAlbumInfo != None:
        # creat outputdir
        title = pathHelper.mkdirs(aAlbumInfo['title'], '-')
        targetDir = cf.outputdir + "\\Album\\" + title
        if os.access(targetDir, 0) == False:
            pathHelper.mkdirs(targetDir)

        # creat volumes dir
        count = 0
        numOfVolumes = int(aAlbumInfo['numberOfVolumes'])
        if numOfVolumes > 1:
            while count < numOfVolumes:
                volumeDir = targetDir + "\\Volume" + str(count)
                if os.access(volumeDir, 0) == False:
                    pathHelper.mkdirs(volumeDir)
                count = count + 1
    
    if aTrackInfo != None:
        targetDir = cf.outputdir + "\\Track\\"
        if os.access(targetDir, 0) == False:
            pathHelper.mkdirs(targetDir)

    if aPlaylistInfo != None:
        title = pathHelper.mkdirs(aPlaylistInfo['title'], '-')
        targetDir = cf.outputdir + "\\Playlist\\" + title
        if os.access(targetDir, 0) == False:
            pathHelper.mkdirs(targetDir)

    if aVideoInfo != None:
        targetDir = cf.outputdir + "\\Video\\"
        if os.access(targetDir, 0) == False:
            pathHelper.mkdirs(targetDir)

    return targetDir


def downloadAlbum():
    tool   = TidalTool()
    cf     = TidalConfig()
    thread = threadHelper.ThreadTool(30)

    while True:
        print("----------------ALBUM------------------")
        sID = myinput("Enter AlbumID（Enter '0' go back）:")
        if sID == '0':
            return

        aAlbumInfo = tool.getAlbum(sID)
        if tool.errmsg != "":
            print("Get AlbumInfo Err!")
            continue

        print("[Title]       %s" % (aAlbumInfo['title']))
        print("[SongNum]     %s\n" % (aAlbumInfo['numberOfTracks']))

        # Get Tracks
        aAlbumTracks = tool.getAlbumTracks(sID)
        if tool.errmsg != "":
            print("Get AlbumTracks Err!")
            return
        # Creat OutputDir
        targetDir = mkdirOutputDir(aAlbumInfo)
        # write msg
        string = tool.convertToString(aAlbumInfo, aAlbumTracks)
        with open(targetDir + "\\AlbumInfo.txt", 'w') as fd:
            fd.write(string)
        # download album tracks
        for item in aAlbumTracks['items']:
            filePath = targetDir + "\\" + item['title'] + ".m4a"
            streamInfo = tool.getStreamUrl(str(item['id']), cf.quality)
            if tool.errmsg != "":
                print("[Err]\t\t" + item['title'] + "(Get Stream Url Err!)")
                continue

            paraList = {'title': item['title'], 'url': streamInfo['url'], 'path': filePath}
            thread.threadStartWait(thradfunc_dltrack, paraList)
        # wait all download thread
        while True:
            if thread.allFree() == True:
                break
            threadHelper.time.sleep(2)
    return

def downloadTrack():
    tool   = TidalTool()
    cf     = TidalConfig()
    thread = threadHelper.ThreadTool(1)

    while True:
        print("----------------TRACK------------------")
        sID = myinput("Enter TrackID（Enter '0' go back）:")
        if sID == '0':
            return

        aTrackInfo = tool.getTrack(sID)
        if tool.errmsg != "":
            print("Get TrackInfo Err!")
            return

        print("[TrackTitle ]       %s" % (aTrackInfo['title']))
        print("[Duration   ]       %s" % (aTrackInfo['duration']))
        print("[TrackNumber]       %s" % (aTrackInfo['trackNumber']))
        print("[Version    ]       %s\n" % (aTrackInfo['version']))
        # Creat OutputDir
        targetDir = mkdirOutputDir(None, aTrackInfo)
        # download
        filePath = targetDir + "\\" + aTrackInfo['title'] + ".m4a"
        streamInfo = tool.getStreamUrl(sID, cf.quality)
        if tool.errmsg != "":
            print("[Err]\t\t" + aTrackInfo['title'] + "(Get Stream Url Err!)")
            continue
        paraList = {'title': aTrackInfo['title'], 'url': streamInfo['url'], 'path': filePath}
        thread.threadStartWait(thradfunc_dltrack, paraList)
        # wait all download thread
        while True:
            if thread.allFree() == True:
                break
            threadHelper.time.sleep(2)
    return

def downloadVideo():
    tool   = TidalTool()
    cf     = TidalConfig()
    thread = threadHelper.ThreadTool(50)

    while True:
        print("----------------VIDEO------------------")
        sID = myinput("Enter VideoID（Enter '0' go back）:")
        if sID == '0':
            return
        # sID = 97246192
        aVideoInfo = tool.getVideo(sID)
        if tool.errmsg != "":
            print("Get VideoInfo Err!")
            continue

        print("[Title      ]       %s" % (aVideoInfo['title']))
        print("[Duration   ]       %s" % (aVideoInfo['duration']))
        print("[TrackNumber]       %s" % (aVideoInfo['trackNumber']))
        print("[Type       ]       %s\n" % (aVideoInfo['type']))

        # Creat OutputDir
        targetDir = mkdirOutputDir(None, None, None, aVideoInfo)
        # download
        filePath = targetDir + "\\" + aVideoInfo['title'] + ".mp4"
        # get resolution
        index = 0
        resolutionList, urlList = tool.getVideoResolutionList(sID)
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

        filePath = targetDir + "\\" + aVideoInfo['title'] + ".mp4"
        filePath = pathHelper.replaceLimiChar(filePath, '-')
        if os.path.exists(filePath) == True:
            os.remove(filePath)
        ffmpegDownloadVideo(urlList[int(index)], filePath)
    return

def ffmpegDownloadVideo(url, filePath):
    print("-----downloading-----")
    cmd = "ffmpeg -i " + url + " -c copy -bsf:a aac_adtstoasc \"" + filePath + "\""
    res = subprocess.call(cmd, shell=False)
    if res != 0:
        print("ffmpeg merge video err!")
        return False
    return True
    

def downloadPlaylist():
    tool   = TidalTool()
    cf     = TidalConfig()
    thread = threadHelper.ThreadTool(50)
    while True:
        print("--------------PLAYLIST-----------------")
        sID = myinput("Enter PlayListID（Enter '0' go back）:")
        if sID == '0':
            return

        aPlaylistInfo = tool.getPlaylist(sID, 300)
        if tool.errmsg != "":
            print("Get PlaylistInfo Err!")
            return

        print("[Title         ]       %s" % (aPlaylistInfo['title']))
        print("[Type          ]       %s" % (aPlaylistInfo['type']))
        print("[Public        ]       %s" % (aPlaylistInfo['public']))
        print("[NumberOfTracks]       %s" % (aPlaylistInfo['numberOfTracks']))
        print("[NumberOfVideos]       %s" % (aPlaylistInfo['numberOfVideos']))
        print("[Duration      ]       %s\n" % (aPlaylistInfo['duration']))

        # Creat OutputDir
        targetDir = mkdirOutputDir(None, None, aPlaylistInfo)
        # download
        # for item in aAlbumTracks['items']:
        #     filePath = targetDir + "\\" + item['title'] + ".m4a"
        #     streamInfo = tool.getStreamUrl(str(item['id']), cf.quality)
        #     if tool.errmsg != "":
        #         print("[Err]\t\t" + item['title'] + "(Get Stream Url Err!)")
        #         continue

        #     paraList = {'title': item['title'],
        #                 'url': streamInfo['url'], 'path': filePath}
        #     thread.threadStartWait(thradfunc_dltrack, paraList)

        # wait all download thread
        while True:
            if thread.allFree() == True:
                break
            threadHelper.time.sleep(2)
    return

def downloadByFile():
    return


