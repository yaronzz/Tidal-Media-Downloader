from aigpy import cmdHelper
from aigpy import systemHelper

def printErr(length, elsestr):
    if systemHelper.isLinux():
        cmdHelper.myprint("[ERR]".ljust(length), cmdHelper.TextColor.Red, None)
        print(elsestr)
    else:
        print("[ERR]".ljust(length) + elsestr)
def printSUCCESS(length, elsestr):
    if systemHelper.isLinux():
        cmdHelper.myprint("[SUCCESS]".ljust(length), cmdHelper.TextColor.Green, None)
        print(elsestr)
    else:
        print("[SUCCESS]".ljust(length) + elsestr)
def printChoice(string, isInt=False, default=None):
    tmpstr = ""
    if systemHelper.isLinux():
        cmdHelper.myprint(string, cmdHelper.TextColor.Yellow, None)
    else:
        tmpstr = string
    if not isInt:
        return cmdHelper.myinput(tmpstr)
    else:
        return cmdHelper.myinputInt(tmpstr, default)
def printMenu():
    if systemHelper.isLinux():
        print("=====================Choice=========================")
        cmdHelper.myprint(" Enter '0': ", cmdHelper.TextColor.Green, None)
        print("Exit.")
        cmdHelper.myprint(" Enter '1': ", cmdHelper.TextColor.Green, None)
        print("LogIn And Get SessionID.")
        cmdHelper.myprint(" Enter '2': ", cmdHelper.TextColor.Green, None)
        print("Setting(OutputDir/Quality/ThreadNum).")
        cmdHelper.myprint(" Enter '3': ", cmdHelper.TextColor.Green, None)
        print("Download Album.")
        cmdHelper.myprint(" Enter '4': ", cmdHelper.TextColor.Green, None)
        print("Download Track.")
        cmdHelper.myprint(" Enter '5': ", cmdHelper.TextColor.Green, None)
        print("Download PlayList.")
        cmdHelper.myprint(" Enter '6': ", cmdHelper.TextColor.Green, None)
        print("Download Video.")
        cmdHelper.myprint(" Enter '7': ", cmdHelper.TextColor.Green, None)
        print("Download Favorite.")
        print("====================================================")
    else:
        print("=====================Choice=========================")
        print(" Enter '0' : Exit")
        print(" Enter '1' : LogIn And Get SessionID.")
        print(" Enter '2' : Setting(OutputDir/Quality/ThreadNum).")
        print(" Enter '3' : Download Album.")
        print(" Enter '4' : Download Track.")
        print(" Enter '5' : Download PlayList.")
        print(" Enter '6' : Download Video")
        print(" Enter '7' : Download Favorite")
        print("====================================================")
