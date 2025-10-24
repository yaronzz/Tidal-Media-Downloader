#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   3.0
@Contact :   yaronhuang@foxmail.com
@Desc    :
'''
import sys
import getopt
import aigpy

from events import *
from listener import start_listener
from settings import *
from gui import startGui
from printf import Printf


def mainCommand():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvgl:o:q:r:",
            ["help", "version", "gui", "link=", "output=", "quality", "resolution", "listen"],
        )
    except getopt.GetoptError as errmsg:
        Printf.err(vars(errmsg)['msg'] + ". Use 'tidal-dl -h' for usage.")
        return

    link = None
    showGui = False

    for opt, val in opts:
        if opt in ('-h', '--help'):
            Printf.usage()
            return
        if opt in ('-v', '--version'):
            Printf.logo()
            return
        if opt in ('-g', '--gui'):
            showGui = True
            continue
        if opt == '--listen':
            start_listener()
            return
        if opt in ('-l', '--link'):
            link = val
            continue
        if opt in ('-o', '--output'):
            SETTINGS.downloadPath = val
            SETTINGS.save()
            continue
        if opt in ('-q', '--quality'):
            SETTINGS.audioQuality = SETTINGS.getAudioQuality(val)
            SETTINGS.save()
            continue
        if opt in ('-r', '--resolution'):
            SETTINGS.videoQuality = SETTINGS.getVideoQuality(val)
            SETTINGS.save()
            continue

    if not aigpy.path.mkdirs(SETTINGS.downloadPath):
        Printf.err(LANG.select.MSG_PATH_ERR + SETTINGS.downloadPath)
        return

    if showGui:
        startGui()
        return

    if link is not None:
        if not loginByConfig():
            if apiSupportsPkce():
                loginByPkce()
            else:
                loginByWeb()
        Printf.info(LANG.select.SETTING_DOWNLOAD_PATH + ':' + SETTINGS.downloadPath)
        start(link)

def main():
    SETTINGS.read(getProfilePath())
    TOKEN.read(getTokenPath())
    TIDAL_API.apiKey = apiKey.getItem(SETTINGS.apiKeyIndex)

    if len(sys.argv) > 1:
        mainCommand()
        return

    Printf.logo()
    Printf.settings()

    if not apiKey.isItemValid(SETTINGS.apiKeyIndex):
        changeApiKey()
        if apiSupportsPkce():
            loginByPkce()
        else:
            loginByWeb()
    elif not loginByConfig():
        if apiSupportsPkce():
            loginByPkce()
        else:
            loginByWeb()

    Printf.checkVersion()

    while True:
        Printf.choices()
        choice = Printf.enter(LANG.select.PRINT_ENTER_CHOICE)
        if choice == "0":
            return
        elif choice == "1":
            if not loginByConfig():
                if apiSupportsPkce():
                    loginByPkce()
                else:
                    loginByWeb()
        elif choice == "2":
            if apiSupportsPkce():
                loginByPkce()
            else:
                loginByWeb()
        elif choice == "3":
            loginByAccessToken()
        elif choice == "4":
            changePathSettings()
        elif choice == "5":
            changeQualitySettings()
        elif choice == "6":
            changeSettings()
        elif choice == "7":
            if changeApiKey():
                if apiSupportsPkce():
                    loginByPkce()
                else:
                    loginByWeb()
        elif choice == "8":
            loginByPkce()
        elif choice == "9":
            start_listener()
        else:
            start(choice)


def test():
    SETTINGS.read(getProfilePath())
    TOKEN.read(getTokenPath())

    if not loginByConfig():
        if apiSupportsPkce():
            loginByPkce()
        else:
            loginByWeb()

    SETTINGS.audioQuality = AudioQuality.Master
    SETTINGS.videoFileFormat = VideoQuality.P240
    SETTINGS.checkExist = False
    SETTINGS.includeEP = True
    SETTINGS.saveCovers = True
    SETTINGS.lyricFile = True
    SETTINGS.showProgress = True
    SETTINGS.showTrackInfo = True
    SETTINGS.saveAlbumInfo = True
    SETTINGS.downloadVideos = True
    SETTINGS.downloadPath = "./download/"
    SETTINGS.usePlaylistFolder = True
    SETTINGS.albumFolderFormat = R"{ArtistName}/{Flag} {AlbumTitle} [{AlbumID}] [{AlbumYear}]"
    SETTINGS.playlistFolderFormat = R"Playlist/{PlaylistName} [{PlaylistUUID}]"
    SETTINGS.trackFileFormat = R"{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
    SETTINGS.videoFileFormat = R"{VideoNumber} - {ArtistName} - {VideoTitle}{ExplicitFlag}"
    SETTINGS.multiThread = False
    SETTINGS.apiKeyIndex = 4
    SETTINGS.checkExist = False

    Printf.settings()

    TIDAL_API.getPlaylistSelf()
    # test example
    # https://tidal.com/browse/track/70973230
    # track 70973230  77798028 212657
    start('242700165')
    # album 58138532  77803199  21993753   79151897  56288918
    # start('58138532')
    # playlist 98235845-13e8-43b4-94e2-d9f8e603cee7
    # start('98235845-13e8-43b4-94e2-d9f8e603cee7')
    # video 155608351 188932980 https://tidal.com/browse/track/55130637
    # start("155608351")https://tidal.com/browse/track/199683732


if __name__ == '__main__':
    # test()
    main()
