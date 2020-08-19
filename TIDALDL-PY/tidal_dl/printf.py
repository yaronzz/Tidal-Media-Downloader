#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   printf.py
@Time    :   2020/08/16
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import prettytable
from aigpy.cmdHelper import red, green, blue, yellow, myprint, myinput, TextColor

__LOGO__ = '''
 /$$$$$$$$ /$$       /$$           /$$               /$$ /$$
|__  $$__/|__/      | $$          | $$              | $$| $$
   | $$    /$$  /$$$$$$$  /$$$$$$ | $$          /$$$$$$$| $$
   | $$   | $$ /$$__  $$ |____  $$| $$ /$$$$$$ /$$__  $$| $$
   | $$   | $$| $$  | $$  /$$$$$$$| $$|______/| $$  | $$| $$
   | $$   | $$| $$  | $$ /$$__  $$| $$        | $$  | $$| $$
   | $$   | $$|  $$$$$$$|  $$$$$$$| $$        |  $$$$$$$| $$
   |__/   |__/ \_______/ \_______/|__/         \_______/|__/
   
       https://github.com/yaronzz/Tidal-Media-Downloader 
'''
VERSION = '2020.8.19.4'

class Printf(object):

    @staticmethod
    def logo():
        print(__LOGO__)
        print('                      v' + VERSION)

    @staticmethod
    def settings(data):
        tb = prettytable.PrettyTable()
        tb.field_names = [green("SETTINGS"), green("VALUE")]
        tb.align = 'l'
        tb.add_row(["Download path", data.downloadPath])
        tb.add_row(["Convert mp4 to m4a", data.onlyM4a])
        tb.add_row(["Add explicit tag", data.addExplicitTag])
        tb.add_row(["Add hyphen", data.addHyphen])
        tb.add_row(["Add user track number", data.useTrackNumber])
        tb.add_row(["Audio quality", data.audioQuality])
        tb.add_row(["Video quality", data.videoQuality])
        tb.add_row(["Check exist", data.checkExist])
        tb.add_row(["ArtistName before track-title", data.artistBeforeTitle])
        tb.add_row(["Id Before album-folder", data.addAlbumIDBeforeFolder])
        tb.add_row(["Include single&ep", data.includeEP])
        tb.add_row(["Save covers", data.saveCovers])
        print(tb)

    @staticmethod
    def choices():
        print("=====================Choice=========================")
        tb = prettytable.PrettyTable()
        tb.field_names = ["CHOICES", "FUNCTION"]
        tb.align = 'l'
        tb.set_style(prettytable.PLAIN_COLUMNS)
        tb.add_row([green("Enter '0':"), "Exit."])
        tb.add_row([green("Enter '1':"), "Login."])
        tb.add_row([green("Enter '2':"), "Settings."])
        tb.add_row([green("Enter '3':"), "Set AccessToken."])
        tb.add_row([green("Enter 'Url/ID':"), "Download by url or id."])
        print(tb)
        print("====================================================")

    @staticmethod
    def enter(string):
        myprint(string, TextColor.Yellow, None)
        ret = myinput("")
        return ret

    @staticmethod
    def err(string):
        print(red("[ERR] ") + string)
    
    @staticmethod
    def info(string):
        print(blue("[INFO] ") + string)

    @staticmethod
    def success(string):
        print(green("[SUCCESS] ") + string)

    @staticmethod
    def album(data):
        tb = prettytable.PrettyTable()
        tb.field_names = [green("ALBUM-PROPERTY"), green("VALUE")]
        tb.align = 'l'
        tb.add_row(["Title", data.title])
        tb.add_row(["Track Number", data.numberOfTracks])
        tb.add_row(["Video Number", data.numberOfVideos])
        tb.add_row(["Release Date", data.releaseDate])
        tb.add_row(["Version", data.version])
        tb.add_row(["Explicit", data.explicit])
        print(tb)

    @staticmethod
    def track(data):
        tb = prettytable.PrettyTable()
        tb.field_names = [green("TRACK-PROPERTY"), green("VALUE")]
        tb.align = 'l'
        tb.add_row(["Title", data.title])
        tb.add_row(["Album", data.album.title])
        tb.add_row(["Version", data.version])
        tb.add_row(["Explicit", data.explicit])
        print(tb)
    
    @staticmethod
    def video(data):
        tb = prettytable.PrettyTable()
        tb.field_names = [green("VIDEO-PROPERTY"), green("VALUE")]
        tb.align = 'l'
        tb.add_row(["Title", data.title])
        tb.add_row(["Album", data.album.title if data.album != None else None])
        tb.add_row(["Version", data.version])
        tb.add_row(["Explicit", data.explicit])
        print(tb)

    @staticmethod
    def artist(data):
        tb = prettytable.PrettyTable()
        tb.field_names = [green("ARTIST-PROPERTY"), green("VALUE")]
        tb.align = 'l'
        tb.add_row(["ID", data.id])
        tb.add_row(["Name", data.name])
        tb.add_row(["Type", str(data.type)])
        print(tb)

    @staticmethod
    def playlist(data):
        tb = prettytable.PrettyTable()
        tb.field_names = [green("PLAYLIST-PROPERTY"), green("VALUE")]
        tb.align = 'l'
        tb.add_row(["Title", data.title])
        tb.add_row(["Track Number", data.numberOfTracks])
        tb.add_row(["Video Number", data.numberOfVideos])
        print(tb)

