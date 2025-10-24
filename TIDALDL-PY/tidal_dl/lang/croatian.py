# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   croatian.py
@Time    :   2020/08/19
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''


class LangCroatian(object):
    SETTING = "POSTAVKE"
    VALUE = "VRIJEDNOST"
    SETTING_DOWNLOAD_PATH = "putanja preuzimanja"
    SETTING_ONLY_M4A = "Pretvori mp4 u m4a"
    SETTING_ADD_EXPLICIT_TAG = "Dodaj eksplicitni znak"
    SETTING_ADD_HYPHEN = "Dodaj crticu"
    SETTING_ADD_YEAR = "Dodaj godinu prije imena albuma u mapi"
    SETTING_USE_TRACK_NUM = "Dodaj korisnicki broj pjesme"
    SETTING_AUDIO_QUALITY = "Kvaliteta zvuka"
    SETTING_VIDEO_QUALITY = "Kvaliteta videozapisa"
    SETTING_CHECK_EXIST = "Provjeri postoji li"
    SETTING_ARTIST_BEFORE_TITLE = "Ime izvodjaca prije imena pjesme"
    SETTING_ALBUMID_BEFORE_FOLDER = "ID oznaka prije imena albuma u mapi"
    SETTING_INCLUDE_EP = "Ukljuci singl i EP"
    SETTING_SAVE_COVERS = "Spremi ilustraciju albuma"
    SETTING_LANGUAGE = "Jezik"
    SETTING_USE_PLAYLIST_FOLDER = "Use playlist folder"
    SETTING_MULITHREAD_DOWNLOAD = "Multi thread download"
    SETTING_ALBUM_FOLDER_FORMAT = "Album folder format"
    SETTING_PLAYLIST_FOLDER_FORMAT = "Playlist folder format"
    SETTING_TRACK_FILE_FORMAT = "Track file format"
    SETTING_VIDEO_FILE_FORMAT = "Video file format"
    SETTING_SHOW_PROGRESS = "Show progress"
    SETTING_SHOW_TRACKINFO = "Show Track Info"
    SETTING_SAVE_ALBUMINFO = "Save AlbumInfo.txt"
    SETTING_DOWNLOAD_VIDEOS = "Download videos"
    SETTING_ADD_LYRICS = "Add lyrics"
    SETTING_LYRICS_SERVER_PROXY = "Lyrics server proxy"
    SETTING_ADD_LRC_FILE = "Save timed lyrics (.lrc file)"
    SETTING_PATH = "Settings path"
    SETTING_APIKEY = "APIKey support"
    SETTING_ADD_TYPE_FOLDER = "Add Type-Folder"
    SETTING_DOWNLOAD_DELAY = "Use Download Delay"
    SETTING_LISTENER_ENABLED = "Listener mode enabled"
    SETTING_LISTENER_PORT = "Listener port"
    SETTING_LISTENER_SECRET = "Listener secret"

    CHOICE = "ODABIR"
    FUNCTION = "FUNKCIJA"
    CHOICE_ENTER = "Ulaz"
    CHOICE_ENTER_URLID = "Unesi 'Url/ID':"
    CHOICE_EXIT = "Izlaz"
    CHOICE_LOGIN = "Check AccessToken"
    CHOICE_SETTINGS = "Postavke"
    CHOICE_SET_ACCESS_TOKEN = "Postavi AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Preuzmi po url-u ili ID-u"
    CHOICE_LOGOUT = "Logout"
    CHOICE_APIKEY = "Select APIKey"
    CHOICE_PKCE_LOGIN = "Login via PKCE"
    CHOICE_LISTENER = "Start listener mode"

    PRINT_ERR = "[ERR]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[USPIJESNO]"

    PRINT_ENTER_CHOICE = "Unesi odabir:"
    PRINT_LATEST_VERSION = "Posljednja verzija:"
    # PRINT_USERNAME = "korisnik:"
    # PRINT_PASSWORD = "lozinka:"

    CHANGE_START_SETTINGS = "Pokreni postavke (0'-Izlaz,'1'-Da):"
    CHANGE_DOWNLOAD_PATH = "Putanja preuzimanja('0' ne mijenjaj):"
    CHANGE_AUDIO_QUALITY = "Kvaliteta zvuka('0'-Normalna,'1'-Visoka,'2'-HiFi,'3'-Master,'4'-Max):"
    CHANGE_VIDEO_QUALITY = "Kvaliteta videozapisa(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Pretvori mp4 u m4a('0'-Ne,'1'-Da):"
    CHANGE_ADD_EXPLICIT_TAG = "Dodaj eksplicitni znak u imeni datoteke('0'-Ne,'1'-Da):"
    CHANGE_ADD_HYPHEN = "Koristi crtice umjesto razmaka u imeni datoteke ('0'-Ne,'1'-Da):"
    CHANGE_ADD_YEAR = "Dodaj godinu u imenu albuma u mapi('0'-Ne,'1'-Da):"
    CHANGE_USE_TRACK_NUM = "Dodaj broj pjesme prije imena pjesme u datoteci ('0'-Ne,'1'-Da):"
    CHANGE_CHECK_EXIST = "Provjeri postoji li ista datoteka prije preuzimanja pjesme('0'-Ne,'1'-Da):"
    CHANGE_ARTIST_BEFORE_TITLE = "Dodaj ime izvodjaca prije imena pjesme('0'-Ne,'1'-Da):"
    CHANGE_INCLUDE_EP = "Ukljuci singlove i EP-ove prilikom preuzimanja albuma izvodjaca('0'-Ne,'1'-Da):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Dodaj ID oznaku prije imena albuma u datoteci('0'-Ne,'1'-Da):"
    CHANGE_SAVE_COVERS = "Spremi ilustracije albuma('0'-Ne,'1'-Da):"
    CHANGE_LANGUAGE = "Odaberi jezik"
    CHANGE_ALBUM_FOLDER_FORMAT = "Album folder format('0'-not modify,'default'-to set default):"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Playlist folder format('0'-not modify,'default'-to set default):"
    CHANGE_TRACK_FILE_FORMAT = "Track file format('0'-not modify,'default'-to set default):"
    CHANGE_VIDEO_FILE_FORMAT = "Video file format('0'-not modify,'default'-to set default):"
    CHANGE_SHOW_PROGRESS = "Show progress('0'-No,'1'-Yes):"
    CHANGE_SHOW_TRACKINFO = "Show track info('0'-No,'1'-Yes):"
    CHANGE_SAVE_ALBUM_INFO = "Save AlbumInfo.txt('0'-No,'1'-Yes):"
    CHANGE_DOWNLOAD_VIDEOS = "Download videos (when downloading playlists, albums, mixes)('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Add lyrics('0'-No,'1'-Yes):"
    CHANGE_LYRICS_SERVER_PROXY = "Lyrics server proxy('0'-not modify):"
    CHANGE_ADD_LRC_FILE = "Save timed lyrics .lrc file ('0'-No,'1'-Yes):"
    CHANGE_ADD_TYPE_FOLDER = "Add Type-Folder,eg Album/Video/Playlist('0'-No,'1'-Yes):"
    CHANGE_MULITHREAD_DOWNLOAD = "Multi thread download('0'-No,'1'-Yes):"
    CHANGE_USE_DOWNLOAD_DELAY = "Use Download Delay('0'-No,'1'-Yes):"
    CHANGE_ENABLE_LISTENER = "Enable listener mode('0'-No,'1'-Yes):"
    CHANGE_LISTENER_SECRET = "Listener secret('0'-not modify):"
    CHANGE_LISTENER_PORT = "Listener port('0'-not modify):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Starting login process..."
    AUTH_LOGIN_CODE = "Your login code is {}"
    AUTH_NEXT_STEP = "Go to {} within the next {} to complete setup."
    AUTH_WAITING = "Waiting for authorization..."
    AUTH_TIMEOUT = "Operation timed out."

    MSG_VALID_ACCESSTOKEN = "AccessToken good for {}."
    MSG_INVALID_ACCESSTOKEN = "Expired AccessToken. Attempting to refresh it."
    MSG_PATH_ERR = "Pogreska putanje!"
    MSG_INPUT_ERR = "Pogreska unosa!"

    MODEL_ALBUM_PROPERTY = "ALBUM-SVOJSTVO"
    MODEL_TRACK_PROPERTY = "PJESMA-SVOJSTVO"
    MODEL_VIDEO_PROPERTY = "VIDEOZAPIS-SVOJSTVO"
    MODEL_ARTIST_PROPERTY = "IZVODJAC-SVOJSTVO"
    MODEL_PLAYLIST_PROPERTY = "PLAYLISTA-SVOJSTVO"

    MODEL_TITLE = 'Naziv'
    MODEL_TRACK_NUMBER = 'Broj pjesme'
    MODEL_VIDEO_NUMBER = 'Broj videozapisa'
    MODEL_RELEASE_DATE = 'Datum izlaska'
    MODEL_VERSION = 'Verzija'
    MODEL_EXPLICIT = 'Eksplicitno'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Naziv'
    MODEL_TYPE = 'Vrsta'
