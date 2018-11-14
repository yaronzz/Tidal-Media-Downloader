import requests
import json

def GetAlbumInfo(sID):
    sUrl = "https://webapi.tidal.com/v1/share/albums/" + sID + "?token=hZ9wuySZCmpLLiui"
    sContent = requests.get(sUrl).content
    aInfo = json.loads(sContent)
    return aInfo

def GetAlbumCoverUrl(sCoverID):
    sUrl = "http://resources.wimpmusic.com/images/" + sCoverID + "/1080x720.jpg"
    return sUrl

def GetAlbumTracks(sID):
    sUrl = "https://webapi.tidal.com/v1/share/albums/" + sID + "/tracks?token=hZ9wuySZCmpLLiui"
    sContent = requests.get(sUrl).content
    aInfo = json.loads(sContent)
    return aInfo

def ConvertAlbumInfoToString(aAlbumInfo, aAlbumTracks):
    str = ""
    str += "[ID]          %d\n" % (aAlbumInfo['id'])
    str += "[Title]       %s\n" % (aAlbumInfo['title'])
    str += "[Artists]     %s\n" % (aAlbumInfo['artist']['name'])
    # str += "[CopyRight]   %s\n" % (aAlbumInfo['copyright'])
    str += "[ReleaseDate] %s\n" % (aAlbumInfo['releaseDate'])
    str += "[SongNum]     %s\n" % (aAlbumInfo['numberOfTracks'])
    str += "[Duration]    %s\n" % (aAlbumInfo['duration'])
    str += '\n'
    return str
