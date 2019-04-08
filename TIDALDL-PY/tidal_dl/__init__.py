import sys
import os

from aigpy import pipHelper
from aigpy import pathHelper
from aigpy.cmdHelper import myinput,myinputInt

import tidal_dl.tidal as tidal
from tidal_dl.tidal import TidalConfig
from tidal_dl.tidal import TidalAccount
from tidal_dl.download import Download
from tidal_dl.printhelper import printMenu,printChoice,printErr

TIDAL_DL_VERSION="2019.4.8.0"

def logIn(username = "", password = ""):
    if username == "" or password == "":
        print("----------------LogIn------------------")
        username = myinput("username:")
        password = myinput("password:")
    account = TidalAccount(username, password)
    if account.errmsg != "":
        printErr(0, account.errmsg)
        return False

    cf = TidalConfig()
    cf.set_account(username, password, account.session_id, account.country_code, account.user_id)
    return True


def setting():
    cf = TidalConfig()
    print("----------------Setting----------------")
    while True:
        outputdir = myinput("outputdir:")
        if os.path.isdir(outputdir) == False:
            printErr(0, "Path is Err!")
            continue
        break
    while True:
        quality = myinput("quality  :")
        if cf.valid_quality(quality) == False:
            printErr(0, "Quality Err,Only Have " + str(tidal.QUALITY))
            continue
        break
    while True:
        threadnum = myinput("threadnum :")
        if cf.valid_threadnum(threadnum) == False:
            printErr(0, "threadnum Err")
            continue
        break

    cf.set_outputdir(outputdir)
    cf.set_quality(quality)
    cf.set_threadnum(threadnum)

    pathHelper.mkdirs(outputdir + "/Album/")
    pathHelper.mkdirs(outputdir + "/Track/")
    pathHelper.mkdirs(outputdir + "/Playlist/")
    pathHelper.mkdirs(outputdir + "/Video/")
    return

def main(argv=None):
    cf = TidalConfig()
    print(tidal.LOG)
    while logIn(cf.username, cf.password) == False:
        pass

    onlineVer = pipHelper.getLastVersion('tidal-dl')
    print("====================Tidal-dl========================")
    print("OutputDir    :\t" + cf.outputdir)
    print("SessionID    :\t" + cf.sessionid)
    print("CountryCode  :\t" + cf.countrycode)
    print("SoundQuality :\t" + cf.quality)
    print("ThreadNum    :\t" + cf.threadnum)
    print("Version      :\t" + TIDAL_DL_VERSION)
    if onlineVer != None:
        print("LastVer      :\t" + onlineVer)
    print("====================================================")

    dl = Download()
    while True:
        printMenu()
        choice = printChoice("Enter Choice:", True, 99)
        if choice == 0:
            return
        elif choice == 1:
            logIn()
            dl = Download(cf.threadnum)
        elif choice == 2:
            setting()
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

# if __name__ == '__main__':
#     main(sys.argv)

__all__ = ['main', 'tidal', 'download']
