import configparser
import os

def GetValue(section, key):
    cf = configparser.ConfigParser()
    cf.read("tidal.ini")
    if cf.has_section(section) == False:
        return
    for item in cf[section]:
        if item == key:
            str = cf.get(section, key)
            return str

def SetValue(section, key, value):
    flag = os.access("tidal.ini", 0)
    if flag == False:
        fp = open("tidal.ini","w")
        fp.close()

    cf = configparser.ConfigParser()
    cf.read("tidal.ini")
    if cf.has_section(section) == False:
        cf[section] = {}
        print("false2")
    cf[section][key] = value
    with open("tidal.ini", "w") as f:
        cf.write(f)


def GetSessionID():
    str = GetValue("BASE", "sessionid")
    if str:
        return str
    return ""


def SetSessionID(value):
    SetValue("BASE", "sessionid", value)

def GetOutputDir():
    str = GetValue("BASE", "outputdir")
    if str:
        return str
    return ".\\"


def SetOutputDir(value):
    SetValue("BASE", "outputdir", value)

def GetCountryCode():
    str = GetValue("BASE", "countrycode")
    if str:
        return str
    return "US"


def SetCountryCode(value):
    SetValue("BASE", "countrycode", value)


def GetSoundQuality():
    str = GetValue("BASE", "soundquality")
    if str:
        return str
    return "LOSSLESS"


def SetSoundQuality(value):
    SetValue("BASE", "soundquality", value)



