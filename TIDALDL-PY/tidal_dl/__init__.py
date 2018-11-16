import requests
import sys
import os
import getopt
import aigpy
sys.path.append('./tidal_dl')
import tidal
import config
import netHelper
import pathHelper

def printHelp():
    print("-a id:\t" + "Download Album.")
    print("-p id:\t" + "Download Playlist.")
    print("-t id:\t" + "Download Track.")
    print("-h:\t" + "Help Message.")
    print("--outputdir=xxx:\t" + "Set outputdir.")
    print("--sessionid=xxx:\t" + "Set sessionid.")
    print("--quality=xxx:\t" + "Set quality.")
    print("--countrycode=xxx:\t" + "Set countrycode.")
    return

def downloadAlbum(sID):
    # 获取专辑信息
    aAlbumInfo = tidal.GetAlbumInfo(sID)
    if aAlbumInfo == None:
        print("Get AlbumInfo Err!")
        return
    if 'id' not in aAlbumInfo:
        print("Get AlbumInfo Err!")
        return
    print("[Title]       %s" % (aAlbumInfo['title']))
    print("[SongNum]     %s" % (aAlbumInfo['numberOfTracks']))

    # 获取曲目
    aAlbumTracks = tidal.GetAlbumTracks(sID)
    if aAlbumTracks == None:
        print("Get AlbumInfo Err!")
        return

    # 创建输出目录
    OUTPUTDIR = config.GetOutputDir()
    targetDir = OUTPUTDIR + "\\Album\\" + aAlbumInfo['title']
    if os.access(targetDir, 0) == False:
        pathHelper.mkdirs(targetDir)

    #创建分碟目录
    count = 0
    numOfVolumes = int(aAlbumInfo['numberOfVolumes'])
    if numOfVolumes > 1:
        while count < numOfVolumes:
            volumeDir = targetDir + "\\Volume" + str(count)
            if os.access(volumeDir, 0) == False:
                pathHelper.mkdirs(volumeDir)
            count = count + 1

    # 写信息
    string = tidal.ConvertAlbumInfoToString(aAlbumInfo, aAlbumTracks)
    with open(targetDir + "\\AlbumInfo.txt", 'w') as fd:
        fd.write(string)

    # 下载封面
    if 'cover' in aAlbumInfo:
        coverPath = targetDir + '\\' + aAlbumInfo['title'] + ".jpg"
        sCoverUrl = tidal.GetAlbumCoverUrl(aAlbumInfo['cover'])
        if False == netHelper.downloadFile(sCoverUrl, coverPath):
            print("Download Cover Err!")

    # 下载曲目
    SESSIONID = config.GetSessionID()
    COUNTRYCODE = config.GetCountryCode()
    SOUNDQUALITY = config.GetSoundQuality()
    for item in aAlbumTracks['items']:
        filePath = targetDir + "\\" + item['title'] + ".m4a"
        url = tidal.GetStreamUrl(str(item['id']), SESSIONID, SOUNDQUALITY, COUNTRYCODE)
        if False == netHelper.downloadFile(url, filePath):
            print("[Err]\t" + item['title'])
        else:
            print("[SUCCESS]\t" + item['title'])
    return

def main(argv=None):

    
    VERSION = '1.0.0.3'
    OUTPUTDIR = config.GetOutputDir()
    SESSIONID = config.GetSessionID()
    COUNTRYCODE = config.GetCountryCode()
    SOUNDQUALITY = config.GetSoundQuality()

    try:
        useOpts, elseArgs = getopt.getopt(sys.argv[1:], "a:p:t:", ["outputdir=", "sessionid=", "quality=", "countrycode="])
    except getopt.GetoptError:
        printHelp()
        return

    if useOpts.__len__ == 0:
        printHelp()
        return  

    for op, value in useOpts:
        if op == "--outputdir":
            OUTPUTDIR = value
            config.SetOutputDir(value)
        elif op == "--sessionid":
            SESSIONID = value
            config.SetSessionID(value)
        elif op == "--quality":
            SOUNDQUALITY = value
            config.SetSoundQuality(value)
        elif op == "--countrycode":
            COUNTRYCODE = value
            config.SetCountryCode(value)

    print("================================================")
    print("Version:\t" + VERSION)
    print("OutputDir:\t" + OUTPUTDIR)
    print("SessionID:\t" + SESSIONID)
    print("CountryCode:\t" + COUNTRYCODE)
    print("SoundQuality:\t" + SOUNDQUALITY)
    print("================================================")

    for op, value in useOpts:
        if op == "-a":
            downloadAlbum(value)
        elif op == "-p":
            output_file = value
        elif op == "-t":
            sys.exit()
        elif op == "-h":
            printHelp()


if __name__ == '__main__':
    main(sys.argv)
