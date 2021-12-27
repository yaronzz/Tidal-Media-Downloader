#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   czech.py
@Time    :   2020/08/20
@Author  :   Tomikk
@Version :   1.0
@Contact :   justtomikk@gmail.com
@Desc    :   
'''


class LangCzech(object):
    SETTING = "Nastavení"
    VALUE = "Hodnota"
    SETTING_DOWNLOAD_PATH = "Umístění staženého souboru"
    SETTING_ONLY_M4A = "Konvertovat mp4 na m4a"
    SETTING_ADD_EXPLICIT_TAG = "Přidat explicitní značku"
    SETTING_ADD_HYPHEN = "Používat pomlčky místo mezer"
    SETTING_ADD_YEAR = "Přidat rok před jméno složky"
    SETTING_USE_TRACK_NUM = "Přidat číslo skladby"
    SETTING_AUDIO_QUALITY = "Kvalita hudby"
    SETTING_VIDEO_QUALITY = "Kvalita videa"
    SETTING_CHECK_EXIST = "Zkontrolovat jestli soubor již existuje"
    SETTING_ARTIST_BEFORE_TITLE = "Jméno interpreta před jménem skladby"
    SETTING_ALBUMID_BEFORE_FOLDER = "Id před složkou alba"
    SETTING_INCLUDE_EP = "Zahrnout single&ep"
    SETTING_SAVE_COVERS = "Uložit obal alba"
    SETTING_LANGUAGE = "Změna jazyka"
    SETTING_USE_PLAYLIST_FOLDER = "Use playlist folder"
    SETTING_MULITHREAD_DOWNLOAD = "Multi thread download"
    SETTING_ALBUM_FOLDER_FORMAT = "Album folder format"
    SETTING_TRACK_FILE_FORMAT = "Track file format"
    SETTING_SHOW_PROGRESS = "Show progress"
    SETTING_SHOW_TRACKIFNO = "Show Track Info"
    SETTING_SAVE_ALBUMINFO = "Save AlbumInfo.txt"
    SETTING_ADD_LYRICS = "Add lyrics"
    SETTING_LYRICS_SERVER_PROXY = "Lyrics server proxy"
    SETTINGS_ADD_LRC_FILE = "Save timed lyrics (.lrc file)"
    SETTING_PATH = "Settings path"
    SETTING_APIKEY = "APIKey support"
    SETTING_ADD_TYPE_FOLDER = "Add Type-Folder"

    CHOICE = "Výběr"
    FUNCTION = "Funkce"
    CHOICE_ENTER = "Enter"
    CHOICE_ENTER_URLID = "Vložit 'Url/ID':"
    CHOICE_EXIT = "Ukončit"
    CHOICE_LOGIN = "Check AccessToken"
    CHOICE_SETTINGS = "Nastavení"
    CHOICE_SET_ACCESS_TOKEN = "Nastavit přístupový token"
    CHOICE_DOWNLOAD_BY_URL = "Stáhnout buď url nebo id"
    CHOICE_LOGOUT = "Logout"
    CHOICE_APIKEY = "Select APIKey"

    PRINT_ERR = "[Error]"
    PRINT_INFO = "[Info]"
    PRINT_SUCCESS = "[Staženo]"

    PRINT_ENTER_CHOICE = "Zvolit volbu:"
    PRINT_LATEST_VERSION = "Nejnovější verze:"
    # PRINT_USERNAME = "přihlašovací jméno:"
    # PRINT_PASSWORD = "heslo"

    CHANGE_START_SETTINGS = "Start settings('0'-Zpět,'1'-Ano):"
    CHANGE_DOWNLOAD_PATH = "Cesta stažení('0' not modify):"
    CHANGE_AUDIO_QUALITY = "Kvalita hudby('0'-Normal,'1'-High,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Kvalita videa(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Konvertovat mp4 na m4a('0'-Ne,'1'-Ano):"
    CHANGE_ADD_EXPLICIT_TAG = "Přidat explicitní značku k souborům('0'-Ne,'1'-Ano):"
    CHANGE_ADD_HYPHEN = "V názvech souborů používat místo mezer pomlčky('0'-Ne,'1'-Ano):"
    CHANGE_ADD_YEAR = "Přidat rok vydání do názvu složky('0'-Ne,'1'-Ano):"
    CHANGE_USE_TRACK_NUM = "Přidat číslo skladby před název skladby('0'-Ne,'1'-Ano):"
    CHANGE_CHECK_EXIST = "Zkontrolovat existujicí soubor před stažením('0'-Ne,'1'-Ano):"
    CHANGE_ARTIST_BEFORE_TITLE = "Přidat jméno interpreta před názvem skladby('0'-Ne,'1'-Ano):"
    CHANGE_INCLUDE_EP = "Při stahování alba interpreta zahrnout singly a EP('0'-Ne,'1'-Ano):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Přidat ID před složku do alba('0'-Ne,'1'-Ano):"
    CHANGE_SAVE_COVERS = "Uložit obaly alb('0'-Ne,'1'-Ano):"
    CHANGE_LANGUAGE = "Zvolit jazyk"
    CHANGE_ALBUM_FOLDER_FORMAT = "Album folder format('0' not modify):"
    CHANGE_TRACK_FILE_FORMAT = "Track file format('0' not modify):"
    CHANGE_SHOW_PROGRESS = "Show progress('0'-No,'1'-Yes):"
    CHANGE_SHOW_TRACKINFO = "Show track info('0'-No,'1'-Yes):"
    CHANGE_SAVE_ALBUM_INFO = "Save AlbumInfo.txt('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Add lyrics('0'-No,'1'-Yes):"
    CHANGE_LYRICS_SERVER_PROXY = "Lyrics server proxy('0' not modify):"
    CHANGE_ADD_LRC_FILE = "Save timed lyrics .lrc file ('0'-No,'1'-Yes):"
    CHANGE_ADD_TYPE_FOLDER = "Add Type-Folder,eg Album/Video/Playlist('0'-No,'1'-Yes):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Starting login process..."
    AUTH_LOGIN_CODE = "Your login code is {}"
    AUTH_NEXT_STEP = "Go to {} within the next {} to complete setup."
    AUTH_WAITING = "Waiting for authorization..."
    AUTH_TIMEOUT = "Operation timed out."

    MSG_VALID_ACCESSTOKEN = "AccessToken good for {}."
    MSG_INVAILD_ACCESSTOKEN = "Expired AccessToken. Attempting to refresh it."
    MSG_PATH_ERR = "Cesta neexistuje!"
    MSG_INPUT_ERR = "Chyba vstupu!"

    MODEL_ALBUM_PROPERTY = "ALBUM-PROPERTY"
    MODEL_TRACK_PROPERTY = "TRACK-PROPERTY"
    MODEL_VIDEO_PROPERTY = "VIDEO-PROPERTY"
    MODEL_ARTIST_PROPERTY = "ARTIST-PROPERTY"
    MODEL_PLAYLIST_PROPERTY = "PLAYLIST-PROPERTY"

    MODEL_TITLE = 'Název skladby'
    MODEL_TRACK_NUMBER = 'Číslo skladby'
    MODEL_VIDEO_NUMBER = 'Číslo videa'
    MODEL_RELEASE_DATE = 'Datum vydání'
    MODEL_VERSION = 'Verze'
    MODEL_EXPLICIT = 'Explicit'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Jméno'
    MODEL_TYPE = 'Typ'
