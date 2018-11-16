import requests
import json

def GetNetInfo(sUrl):
    try:
        re = requests.get(sUrl, timeout=(3.05, 27))
        aInfo = json.loads(re.content)
        return aInfo
    except:
        return

def GetAlbumInfo(sID):
    sUrl = "https://webapi.tidal.com/v1/share/albums/" + sID + "?token=hZ9wuySZCmpLLiui"
    return GetNetInfo(sUrl)

def GetAlbumCoverUrl(sCoverID):
    sUrl = "http://resources.wimpmusic.com/images/" + sCoverID + "/1080x720.jpg"
    return sUrl

def GetAlbumTracks(sID):
    sUrl = "https://webapi.tidal.com/v1/share/albums/" + sID + "/tracks?token=hZ9wuySZCmpLLiui"
    return GetNetInfo(sUrl)


def GetStreamUrl(sID, sSessionID, sSoundQuality, sCountryCode):
    sUrl = "https://api.tidal.com/v1/tracks/" + sID + "/streamurl?sessionId=" + sSessionID + "&soundQuality=" + sSoundQuality + "&countryCode=" + sCountryCode
    ajson = GetNetInfo(sUrl)
    if ajson != None:
        return ajson['url']

def ConvertAlbumInfoToString(aAlbumInfo, aAlbumTracks):
    str = ""
    if 'id' not in aAlbumInfo:
        return ""

    str += "[ID]          %d\n" % (aAlbumInfo['id'])
    str += "[Title]       %s\n" % (aAlbumInfo['title'])
    str += "[Artists]     %s\n" % (aAlbumInfo['artist']['name'])
    # str += "[CopyRight]   %s\n" % (aAlbumInfo['copyright'])
    str += "[ReleaseDate] %s\n" % (aAlbumInfo['releaseDate'])
    str += "[SongNum]     %s\n" % (aAlbumInfo['numberOfTracks'])
    str += "[Duration]    %s\n" % (aAlbumInfo['duration'])
    str += '\n'
    return str
