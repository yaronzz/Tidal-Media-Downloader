#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   danish.py
@Time    :   2021/03/25
@Author  :   KB885
@Version :   1.0
@Contact :   
@Desc    :   
'''


class LangDanish(object):
    SETTING = "INDSTILLINGER"
    VALUE = "Værdi"
    SETTING_DOWNLOAD_PATH = "Download sti"
    SETTING_ONLY_M4A = "Konverter mp4 til m4a"
    SETTING_ADD_EXPLICIT_TAG = "Tilføj eksplicit tag"
    SETTING_ADD_HYPHEN = "Tilføj bindestreg"
    SETTING_ADD_YEAR = "Tilføj år før album mappe"
    SETTING_USE_TRACK_NUM = "Tilføj titelnummer"
    SETTING_AUDIO_QUALITY = "Lydkvalitet"
    SETTING_VIDEO_QUALITY = "Videokvalitet"
    SETTING_CHECK_EXIST = "Kontroller eksistens"
    SETTING_ARTIST_BEFORE_TITLE = "Kunstnernavn før titelnummer"
    SETTING_ALBUMID_BEFORE_FOLDER = "Id før album mappe"
    SETTING_INCLUDE_EP = "Inkluder single&ep"
    SETTING_SAVE_COVERS = "Gem omslag"
    SETTING_LANGUAGE = "Sprog"
    SETTING_USE_PLAYLIST_FOLDER = "Brug afspilningsmappen"
    SETTING_MULITHREAD_DOWNLOAD = "Flertråede download"
    SETTING_ALBUM_FOLDER_FORMAT = "Albummappens format"
    SETTING_TRACK_FILE_FORMAT = "Musiknummerets filformat"
    SETTING_SHOW_PROGRESS = "Vis fremskridt"
    SETTING_SHOW_TRACKIFNO = "Show Track Info"
    SETTING_SAVE_ALBUMINFO = "Save AlbumInfo.txt"
    SETTING_ADD_LYRICS = "Add lyrics"
    SETTING_LYRICS_SERVER_PROXY = "Lyrics server proxy"
    SETTING_PATH = "Settings path"
    SETTINGS_ADD_LRC_FILE = "Save timed lyrics (.lrc file)"
    SETTING_APIKEY = "APIKey support"
    SETTING_ADD_TYPE_FOLDER = "Add Type-Folder"

    CHOICE = "VALG"
    FUNCTION = "FUNKTION"
    CHOICE_ENTER = "Indtast"
    CHOICE_ENTER_URLID = "Indtast 'Url/ID':"
    CHOICE_EXIT = "Afslut"
    CHOICE_LOGIN = "Kontroller AccessToken"
    CHOICE_SETTINGS = "Indstillinger"
    CHOICE_SET_ACCESS_TOKEN = "Sæt AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Download via url eller id"
    CHOICE_LOGOUT = "Log ud"
    CHOICE_APIKEY = "Select APIKey"

    PRINT_ERR = "[FEJL]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[SUCCES]"

    PRINT_ENTER_CHOICE = "Indtast Valg:"
    PRINT_LATEST_VERSION = "Seneste version:"
    # PRINT_USERNAME = "username:"
    # PRINT_PASSWORD = "password:"

    CHANGE_START_SETTINGS = "Start indstillinger('0'-Tilbage,'1'-Ja):"
    CHANGE_DOWNLOAD_PATH = "Download stil('0' ændrer ikke):"
    CHANGE_AUDIO_QUALITY = "Lydkvalitet('0'-Normal,'1'-Høj,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Videokvalitet(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Konverter mp4 til m4a('0'-Nej,'1'-Ja):"
    CHANGE_ADD_EXPLICIT_TAG = "Tilføj eksplicit tag til filnavne('0'-Nej,'1'-Ja):"
    CHANGE_ADD_HYPHEN = "Brug bindestreger i stedet for mellemrum i filnavne('0'-Nej,'1'-Ja):"
    CHANGE_ADD_YEAR = "Tilføj år til albumnavne('0'-Nej,'1'-Ja):"
    CHANGE_USE_TRACK_NUM = "Tilføj titelnummer før filnavne('0'-Nej,'1'-Ja):"
    CHANGE_CHECK_EXIST = "Kontrollér filens eksistens før download('0'-Nej,'1'-Ja):"
    CHANGE_ARTIST_BEFORE_TITLE = "Tilføj kunsternavn før titlenummer('0'-Nej,'1'-Ja):"
    CHANGE_INCLUDE_EP = "Inkluder singler og EP'er når der downloades en kunstners album('0'-Nej,'1'-Ja):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Tilføj id før albummappe('0'-Nej,'1'-Ja):"
    CHANGE_SAVE_COVERS = "Gem omslag('0'-Nej,'1'-Ja):"
    CHANGE_LANGUAGE = "Vælg sprog"
    CHANGE_ALBUM_FOLDER_FORMAT = "Albummappeformat('0' Ændrer ikke, 'default' for at indstille som standard):"
    CHANGE_TRACK_FILE_FORMAT = "Musiknummerets filformat('0' Ændrer ikke, 'default' for at indstille som standard):"
    CHANGE_SHOW_PROGRESS = "Vis fremskridt('0'-Nej,'1'-Ja):"
    CHANGE_SHOW_TRACKINFO = "Show track info('0'-No,'1'-Yes):"
    CHANGE_SAVE_ALBUM_INFO = "Save AlbumInfo.txt('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Add lyrics('0'-No,'1'-Yes):"
    CHANGE_LYRICS_SERVER_PROXY = "Lyrics server proxy('0' not modify):"
    CHANGE_ADD_LRC_FILE = "Save timed lyrics .lrc file ('0'-No,'1'-Yes):"
    CHANGE_ADD_TYPE_FOLDER = "Add Type-Folder,eg Album/Video/Playlist('0'-No,'1'-Yes):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Starter login-processen."
    AUTH_LOGIN_CODE = "Din login kode er {}"
    AUTH_NEXT_STEP = "Gå til {} inden for de næste {} for at afslutte opsætningen."
    AUTH_WAITING = "Venter på godkendelse..."
    AUTH_TIMEOUT = "Tiden løb ud."

    MSG_VALID_ACCESSTOKEN = "AccessToken tilgængelig for {}."
    MSG_INVAILD_ACCESSTOKEN = "AccessToken udløb. Forsøger at opdatere"
    MSG_PATH_ERR = "Sti fejl!"
    MSG_INPUT_ERR = "Indtastningsfejl!"

    MODEL_ALBUM_PROPERTY = "ALBUM-PROPERTY"
    MODEL_TRACK_PROPERTY = "TRACK-PROPERTY"
    MODEL_VIDEO_PROPERTY = "VIDEO-PROPERTY"
    MODEL_ARTIST_PROPERTY = "ARTIST-PROPERTY"
    MODEL_PLAYLIST_PROPERTY = "PLAYLIST-PROPERTY"

    MODEL_TITLE = 'Titel'
    MODEL_TRACK_NUMBER = 'Titelnummer'
    MODEL_VIDEO_NUMBER = 'Videonummer'
    MODEL_RELEASE_DATE = 'Udgivelses dato'
    MODEL_VERSION = 'Version'
    MODEL_EXPLICIT = 'Eksplicit'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Navn'
    MODEL_TYPE = 'Type'
