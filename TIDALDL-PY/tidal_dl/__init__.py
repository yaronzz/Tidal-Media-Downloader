import sys
import os

import tidal_dl.tidal as tidal
from tidal_dl.tidal import TidalConfig, TidalAccount
from tidal_dl.download import downloadAlbum, downloadTrack, downloadPlaylist, downloadByFile, downloadVideo
from aigpy.cmdHelper import myinput


def logIn():
    print("----------------LogIn------------------")
    username = myinput("username:")
    password = myinput("password:")
    account = TidalAccount(username, password)
    if account.errmsg != "":
        print(account.errmsg)
        return

    cf = TidalConfig()
    cf.set_account(username, password, account.session_id,
                   account.country_code)
    return


def setting():
    cf = TidalConfig()
    print("----------------Setting----------------")
    while True:
        outputdir = myinput("outputdir:")
        if os.path.isdir(outputdir) == False:
            print("Path is Err!")
            continue
        break
    while True:
        quality = myinput("quality  :")
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
    print("====================Tidal-dl========================")
    print("OutputDir    :\t" + cf.outputdir)
    print("SessionID    :\t" + cf.sessionid)
    print("CountryCode  :\t" + cf.countrycode)
    print("SoundQuality :\t" + cf.quality)
    print("====================================================")

    if cf.sessionid == "":
        logIn()

    while True:
        print("=====================Choice=========================")
        print(" Enter '0' : Exit")
        print(" Enter '1' : LogIn And Get SessionID.")
        print(" Enter '2' : Setting(OutputDir/Quality).")
        print(" Enter '3' : Download Album.")
        print(" Enter '4' : Download Track.")
        # print(" Enter '5' : Download PlayList.")
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
            downloadAlbum()
        elif choice == '4':
            downloadTrack()
        # elif choice == '5':
        #     downloadPlaylist()
        elif choice == '6':
            downloadVideo()
        elif choice == '7':
            downloadByFile()

# if __name__ == '__main__':
#     main(sys.argv)


__all__ = ['main', 'tidal', 'download']
