import sys
import os

from aigpy import pathHelper
from aigpy.cmdHelper import myinput

import tidal_dl.tidal as tidal
from tidal_dl.tidal import TidalConfig
from tidal_dl.tidal import TidalAccount
from tidal_dl.download import Download

def logIn():
    print("----------------LogIn------------------")
    username = myinput("username:")
    password = myinput("password:")
    account = TidalAccount(username, password)
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
        outputdir = myinput("outputdir:")
        if os.path.isdir(outputdir) == False:
            print("[Err]Path is Err!")
            continue
        break
    while True:
        quality = myinput("quality  :")
        if cf.valid_quality(quality) == False:
            print("[Err]Quality Err,Only Have " + str(tidal.QUALITY))
            continue
        break

    cf.set_outputdir(outputdir)
    cf.set_quality(quality)

    pathHelper.mkdirs(outputdir + "\\Album\\")
    pathHelper.mkdirs(outputdir + "\\Track\\")
    pathHelper.mkdirs(outputdir + "\\Playlist\\")
    pathHelper.mkdirs(outputdir + "\\Video\\")
    return

def main(argv=None):
    cf = TidalConfig()
    print(tidal.LOG)
    print("====================Tidal-dl========================")
    print("OutputDir    :\t" + cf.outputdir)
    print("SessionID    :\t" + cf.sessionid)
    print("CountryCode  :\t" + cf.countrycode)
    print("SoundQuality :\t" + cf.quality)
    print("====================================================")

    if cf.sessionid == "":
        logIn()

    dl = Download()
    while True:
        print("=====================Choice=========================")
        print(" Enter '0' : Exit")
        print(" Enter '1' : LogIn And Get SessionID.")
        print(" Enter '2' : Setting(OutputDir/Quality).")
        print(" Enter '3' : Download Album.")
        print(" Enter '4' : Download Track.")
        print(" Enter '5' : Download PlayList.")
        print(" Enter '6' : Download Video")
        # print(" Enter '7' : Download By File")
        print("====================================================")
        choice = myinput("Choice:")
        if choice == '0':
            return
        elif choice == '1':
            logIn()
        elif choice == '2':
            setting()
        elif choice == '3':
            dl.downloadAlbum()
        elif choice == '4':
            dl.downloadTrack()
        elif choice == '5':
            dl.downloadPlaylist()
        elif choice == '6':
            dl.downloadVideo()
        # elif choice == '7':
        #     dl.downloadByFile()

# if __name__ == '__main__':
#     main(sys.argv)


__all__ = ['main', 'tidal', 'download']
