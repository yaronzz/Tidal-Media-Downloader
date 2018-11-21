import sys
import os
import getopt
from aigpy import pathHelper
from aigpy import netHelper

sys.path.append('./tidal_dl')
import tidal_dl.tidal as tidal
from tidal_dl.tidal import TidalConfig,TidalTool,TidalAccount

def downloadAlbum():
    tool = TidalTool()
    cf   = TidalConfig()
    while True:
        print("----------------ALBUM------------------")
        sID = input("Enter AlbumID（Enter '0' go back）:")
        if sID == '0':
            return

        aAlbumInfo = tool.getAlbum(sID)
        if tool.errmsg != "":
            print("Get AlbumInfo Err!")
            return

        print("[Title]       %s" % (aAlbumInfo['title']))
        print("[SongNum]     %s" % (aAlbumInfo['numberOfTracks']))

        # 获取曲目
        aAlbumTracks = tool.getAlbumTracks(sID)
        if tool.errmsg != "":
            print("Get AlbumTracks Err!")
            return

        # 创建输出目录
        targetDir = cf.outputdir + "\\Album\\" + aAlbumInfo['title']
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
        string = tool.convertToString(aAlbumInfo, aAlbumTracks)
        with open(targetDir + "\\AlbumInfo.txt", 'w') as fd:
            fd.write(string)

        # # 下载封面
        # if 'cover' in aAlbumInfo:
        #     coverPath = targetDir + '\\' + aAlbumInfo['title'] + ".jpg"
        #     sCoverUrl = tidal.GetAlbumCoverUrl(aAlbumInfo['cover'])
        #     if False == netHelper.downloadFile(sCoverUrl, coverPath):
        #         print("Download Cover Err!")

        # 下载曲目
        for item in aAlbumTracks['items']:
            filePath   = targetDir + "\\" + item['title'] + ".m4a"
            streamInfo = tool.getStreamUrl(str(item['id']), cf.quality)
            if tool.errmsg != "":
                print("[Err]\t\t" + item['title'] + "(Get Stream Url Err!)")
                continue

            if False == netHelper.downloadFile(streamInfo['url'], filePath):
                print("[Err]\t\t" + item['title'] + "(Download Err!)")
            else:
                print("[SUCCESS]\t\t" + item['title'])
    return

def logIn():
    print("----------------LogIn------------------")
    username = input("username:")
    password = input("password:")
    account  = TidalAccount(username, password)
    if account.errmsg != "":
        print(account.errmsg)
        return

    cf = TidalConfig()
    cf.set_account(username, password, account.session_id, account.country_code)
    return

def setting():
    cf = TidalConfig()
    print("----------------Setting----------------")
    while True:
        outputdir = input("outputdir:")
        if os.path.isdir(outputdir) == False:
            print("Path is Err!")
            continue
        break
    while True:        
        quality = input("quality  :")
        if cf.valid_quality(quality) == False:
            print("[Err]Quality Err,Only Have " + str(tidal.QUALITY))
            continue
        break

    cf = TidalConfig()
    cf.set_outputdir(outputdir)
    cf.set_quality(quality)

def main(argv=None):
    cf = TidalConfig()
    print(tidal.LOG)
    print("================Tidal-dl========================")
    print("OutputDir    :\t" + cf.outputdir)
    print("SessionID    :\t" + cf.sessionid)
    print("CountryCode  :\t" + cf.countrycode)
    print("SoundQuality :\t" + cf.quality)
    print("================================================")

    if cf.sessionid == "":
        logIn()

    while True:
        print("=====================Choice=====================")
        print(" Enter '0' : Exit")
        print(" Enter '1' : LogIn And Get SessionID.")
        print(" Enter '2' : Setting(OutputDir/Quality).")
        print(" Enter '3' : Download Album.")
        # print(" Enter '4' : Download Track.")
        # print(" Enter '5' : Download PlayList.")
        # print(" Enter '6' : Download Albums By File")
        print("================================================")
        choice = input("Choice:")
        if choice == '0':
            return
        elif choice == '1':
            logIn()
        elif choice == '2':
            setting()
        elif choice == '3':
            downloadAlbum()

if __name__ == '__main__':
    main(sys.argv)
