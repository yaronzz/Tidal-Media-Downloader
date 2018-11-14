import configparser

def GetValue(section, key):
    cf = configparser.ConfigParser()
    cf.read("tidal.ini")
    if cf.has_section(section):
        str = cf.get(section, key)
        return str

def GetOutputDir():
    str = GetValue("BASE", "outputDir")
    if str:
        return str
    return ".\\"
