import requests
import sys
import getopt
import tidal
import config

outputDir = config.GetOutputDir()
useOpts, elseArgs = getopt.getopt(sys.argv[1:], "a:p:t:", ["outputdir=", "sessionid=", "quality=", "countrycode="])
for op, value in useOpts:
    if op == "-a":
        aAlbumInfo = tidal.GetAlbumInfo(value)
        aAlbumTracks = tidal.GetAlbumTracks(value)
        sCoverUrl = tidal.GetAlbumCoverUrl(aAlbumInfo['cover'])
        string = tidal.ConvertAlbumInfoToString(aAlbumInfo, aAlbumTracks)
        print(string)
    elif op == "-p":
        output_file = value
    elif op == "-t":
        sys.exit()




