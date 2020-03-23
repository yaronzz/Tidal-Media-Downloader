# -*- coding: utf-8 -*-
import sys
import os

from aigpy import pipHelper
from aigpy import pathHelper
from aigpy.cmdHelper import myinput, myinputInt

from tidal_dl.tidal import TidalConfig
from tidal_dl.tidal import TidalAccount
from tidal_dl.download import Download
from tidal_dl.printhelper import printMenu, printChoice2, printErr, printWarning, LOG

TIDAL_DL_VERSION = "2020.3.23.0"


def logIn(username="", password=""):
    if username == "" or password == "":
        print("----------------LogIn------------------")
        username = myinput("username:")
        password = myinput("password:")
    account = TidalAccount(username, password)
    account2 = TidalAccount(username, password, True)
    if account.errmsg != "":
        printErr(0, account.errmsg)
        return False
    if account2.errmsg != "":
        printErr(0, account2.errmsg)
        return False

    cf = TidalConfig()
    cf.set_account(username, password, account.session_id, account.country_code, account.user_id, account2.session_id)
    return True


def showConfig():
    cf = TidalConfig()
    print("----------------Config------------------")
    print("Username                         : " + cf.username)
    print("Output directory                 : " + cf.outputdir)
    print("SessionID                        : " + cf.sessionid)
    print("Country Code                     : " + cf.countrycode)
    print("Sound Quality                    : " + cf.quality)
    print("Video Resolution                 : " + cf.resolution)
    print("Download Threads                 : " + cf.threadnum)
    print("Only M4a                         : " + cf.onlym4a)
    print("Show download progress           : " + cf.showprogress + "(enable when threadnum=1)")
    print("Use hyphens                      : " + cf.addhyphen + "(between number and title)")
    print("Add year                         : " + cf.addyear + "(in album title)")
    print("Add explicit tag                 : " + cf.addexplicit)
    print("Playlist songs in artist folders : " + cf.plfile2arfolder + "(organized with artist folder)")
    print("Include singles                  : " + cf.includesingle + "(download artist album)")
    print("Save covers                      : " + cf.savephoto)
    print("Version                          : " + TIDAL_DL_VERSION)
    myinput("Enter to return.")


def setting():
    cf = TidalConfig()
    print("----------------Settings----------------")
    print("Output directory                 :\t" + cf.outputdir)
    print("Sound Quality                    :\t" + cf.quality)
    print("Video Resolution                 :\t" + cf.resolution)
    print("Download Threads                 :\t" + cf.threadnum)
    print("Only M4a                         :\t" + cf.onlym4a)
    print("Show download progress           :\t" + cf.showprogress + "(enable when threadnum=1)")
    print("Use hyphens                      :\t" + cf.addhyphen + "(between number and title)")
    print("Add year                         :\t" + cf.addyear + "(in album title)")
    print("Add explicit tag                 :\t" + cf.addexplicit)
    print("Playlist songs in artist folders :\t" + cf.plfile2arfolder + "(organized with artist folder)")
    print("Include singles                  :\t" + cf.includesingle + "(download artist album)")
    print("Save covers                      : " + cf.savephoto)
    while True:
        outputdir = myinput("Output directory(Enter '0' Unchanged):".ljust(12))
        if outputdir == '0':
            outputdir = cf.outputdir
            break
        if os.path.isdir(outputdir) == False:
            printErr(0, "Path is Err!")
            continue
        break
    while True:
        index = myinputInt("Download Quality(0-LOW,1-HIGH,2-LOSSLESS,3-HI_RES):".ljust(12), 999)
        if index > 3 or index < 0:
            printErr(0, "Quality Err!")
            continue
        if index == 0:
            quality = 'LOW'
        if index == 1:
            quality = 'HIGH'
        if index == 2:
            quality = 'LOSSLESS'
        if index == 3:
            quality = 'HI_RES'
        break
    while True:
        index = myinputInt("Video resolution(0-1080,1-720,2-480,3-360,4-240):".ljust(12), 99)
        if index > 4 or index < 0:
            printErr(0, "Resolution Err")
            continue
        if index == 0:
            resolution = '1080'
        if index == 1:
            resolution = '720'
        if index == 2:
            resolution = '480'
        if index == 3:
            resolution = '360'
        if index == 4:
            resolution = '240'
        break
    while True:
        threadnum = myinput("Number of download threads:".ljust(12))
        if cf.valid_threadnum(threadnum) == False:
            printErr(0, "ThreadNum Err")
            continue
        break

    status = myinputInt("Convert Mp4 to M4a(0-No, 1-Yes):".ljust(12), 0)
    status2 = myinputInt("Show download progress (only available on single thread)(0-No, 1-Yes):".ljust(12), 0)
    status3 = myinputInt("Use hyphens instead of spaces in file names(0-No, 1-Yes):".ljust(12), 0)

    while True:
        index = myinputInt("Add year to album folder names(0-No, 1-Before, 2-After):".ljust(12), 99)
        if index > 2 or index < 0:
            printErr(0, "Addyear input Err")
            continue
        if index == 0:
            addyear = 'No'
        if index == 1:
            addyear = 'Before'
        if index == 2:
            addyear = 'After'
        break

    status5 = myinputInt("Download playlist songs in artist folder structure? (0-No,1-Yes):".ljust(12), 0)
    status6 = myinputInt("Add explicit tag to file names(0-No, 1-Yes):".ljust(12), 0)
    status7 = myinputInt("Include singles and EPs when downloading an artist's albums (0-No, 1-Yes):".ljust(12), 0)
    status8 = myinputInt("Save covers(0-No, 1-Yes):".ljust(12), 0)

    cf.set_outputdir(outputdir)
    cf.set_quality(quality)
    cf.set_resolution(resolution)
    cf.set_threadnum(threadnum)
    cf.set_onlym4a(status)
    cf.set_showprogress(status2)
    cf.set_addhyphen(status3)
    cf.set_addyear(addyear)
    cf.set_plfile2arfolder(status5)
    cf.set_addexplicit(status6)
    cf.set_includesingle(status7)
    cf.set_savephoto(status8)

    pathHelper.mkdirs(outputdir + "/Album/")
    pathHelper.mkdirs(outputdir + "/Playlist/")
    pathHelper.mkdirs(outputdir + "/Video/")
    pathHelper.mkdirs(outputdir + "/Favorite/")
    return


def main(argv=None):
    print(LOG)
    cf = TidalConfig()
    if logIn(cf.username, cf.password) == False:
        while logIn("", "") == False:
            pass

    cf = TidalConfig()
    onlineVer = pipHelper.getLastVersion('tidal-dl')
    print("====================Tidal-dl========================")
    print("Output directory                 : " + cf.outputdir)
    print("Sound Quality                    : " + cf.quality)
    print("Video Resolution                 : " + cf.resolution)
    print("Download Threads                 : " + cf.threadnum)
    print("Only M4a                         : " + cf.onlym4a)
    print("Show download progress           : " + cf.showprogress + "(enable when threadnum=1)")
    print("Use hyphens                      : " + cf.addhyphen + "(between number and title)")
    print("Add year                         : " + cf.addyear + "(in album title)")
    print("Add explicit tag                 : " + cf.addexplicit)
    print("Playlist songs in artist folders : " + cf.plfile2arfolder + "(organized with artist folder)")
    print("Include singles                  : " + cf.includesingle + "(download artist album)")
    print("Save covers                      : " + cf.savephoto)
    print("Current Version                  : " + TIDAL_DL_VERSION)
    if onlineVer != None:
        print("Latest Version                   : " + onlineVer)
    print("====================================================")

    dl = Download(cf.threadnum)
    if not dl.ffmpeg.enable:
        printWarning(0, "Couldn't find ffmpeg!\n")
    while True:
        printMenu()
        strchoice, choice = printChoice2("Enter Choice:", 99)
        if choice == 0:
            return
        elif choice == 1:
            logIn()
            cf = TidalConfig()
            dl = Download(cf.threadnum)
        elif choice == 2:
            setting()
            cf = TidalConfig()
            dl = Download(cf.threadnum)
        elif choice == 3:
            dl.downloadAlbum()
        elif choice == 4:
            dl.downloadTrack()
        elif choice == 5:
            dl.downloadPlaylist()
        elif choice == 6:
            dl.downloadVideo()
        elif choice == 7:
            dl.downloadFavorite()
        elif choice == 8:
            dl.downloadArtistAlbum(cf.includesingle == "True")
        elif choice == 9: 
            showConfig()
        #Hidden Code For Developer [200-299]
        elif choice == 200:
            dl.downloadArtistAlbum(False)
        else:
            dl.downloadUrl(strchoice)
            dl.downloadByFile(strchoice)

def debug():
    # cf = TidalConfig()
    # while logIn(cf.username, cf.password) == False:
    #     pass
    # add tag Credits,Info song and full tag (discnumber,irsc,composer,arrenger,publisher,replayGain,releasedate)
    # https://api.tidal.com/v1/albums/71121869/tracks?token=wdgaB1CilGA-S_s2&countryCode=TH
    print('\nThis is the debug version!!\n')
    # os.system("pip install aigpy --upgrade")

    dl = Download(1)
    dl.downloadAlbum("120929182", True)
    # dl.tool.getPlaylist("36ea71a8-445e-41a4-82ab-6628c581535d")
    # ss = dl.tool.getPlaylistArtworkUrl("36ea71a8-445e-41a4-82ab-6628c581535d")
    # ss = dl.tool.getPlaylistArtworkUrl("36ea71a8-445e-41a4-82ab-6628c581535d",480)
    # dl.downloadVideo(57261945) #1hours
    # tidal.com/browse/track/125155002 dubi
    dl.downloadVideo(84094460)

# if __name__ == '__main__':
#     main(sys.argv)


__all__ = ['debug', 'main', 'tidal', 'download']
