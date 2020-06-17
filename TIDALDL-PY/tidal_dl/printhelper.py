# -*- coding: utf-8 -*-
from aigpy import cmdHelper
from aigpy import systemHelper

def printErr(length, elsestr):
    cmdHelper.myprint("[ERR]".ljust(length), cmdHelper.TextColor.Red, None)
    print(elsestr)


def printWarning(length, elsestr):
    cmdHelper.myprint("[WARNING]".ljust(length), cmdHelper.TextColor.Red, None)
    print(elsestr)

def printInfo(length, elsestr):
    cmdHelper.myprint("[INFO]".ljust(length), cmdHelper.TextColor.Yellow, None)
    print(elsestr)

def printSUCCESS(length, elsestr):
    cmdHelper.myprint("[SUCCESS]".ljust(length), cmdHelper.TextColor.Green, None)
    print(elsestr)

def printChoice(string, isInt=False, default=None):
    tmpstr = ""
    cmdHelper.myprint(string, cmdHelper.TextColor.Yellow, None)
    if not isInt:
        return cmdHelper.myinput(tmpstr)
    else:
        return cmdHelper.myinputInt(tmpstr, default)
def printChoice2(string, default=None):
    ret = printChoice(string, False, default)
    try:
        iret = int(ret)
        return ret, iret
    except:
        return ret, default
def printMenu():
    print("=====================Choice=========================")
    cmdHelper.myprint(" Enter '0' : ", cmdHelper.TextColor.Green, None)
    print("Exit.")
    cmdHelper.myprint(" Enter '1' : ", cmdHelper.TextColor.Green, None)
    print("LogIn And Get SessionID.")
    cmdHelper.myprint(" Enter '2' : ", cmdHelper.TextColor.Green, None)
    print("Change Settings.")
    cmdHelper.myprint(" Enter '3' : ", cmdHelper.TextColor.Green, None)
    print("Download an Album.")
    cmdHelper.myprint(" Enter '4' : ", cmdHelper.TextColor.Green, None)
    print("Download a Track.")
    cmdHelper.myprint(" Enter '5' : ", cmdHelper.TextColor.Green, None)
    print("Download a PlayList.")
    cmdHelper.myprint(" Enter '6' : ", cmdHelper.TextColor.Green, None)
    print("Download a Video.")
    cmdHelper.myprint(" Enter '7' : ", cmdHelper.TextColor.Green, None)
    print("Download a Favorite.")
    cmdHelper.myprint(" Enter '8' : ", cmdHelper.TextColor.Green, None)
    print("Download All Albums by an Artist.")
    cmdHelper.myprint(" Enter '9' : ", cmdHelper.TextColor.Green, None)
    print("Show Current Config.")
    cmdHelper.myprint(" Enter URL : ", cmdHelper.TextColor.Green, None)
    print("Download By URL.")
    cmdHelper.myprint(" Enter Path: ", cmdHelper.TextColor.Green, None)
    print("Download By File.")
    print("====================================================")
    

LOG = '''
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
