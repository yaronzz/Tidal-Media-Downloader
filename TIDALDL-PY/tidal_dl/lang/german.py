#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   german.py
@Time    :   2020/10/01
@Author  :   Sematre
@Version :   1.0
@Contact :   
@Desc    :   
'''

class LangGerman(object):
    SETTING = "EINSTELLUNG"
    VALUE = "WERT"
    SETTING_DOWNLOAD_PATH = "Download Pfad"
    SETTING_ONLY_M4A = "mp4 in m4a konvertieren"
    SETTING_ADD_EXPLICIT_TAG = "Explicit Tag hinzufügen"
    SETTING_ADD_HYPHEN = "Bindestrich hinzufügen"
    SETTING_ADD_YEAR = "Jahr vor Album-Ordner hinzufügen"
    SETTING_USE_TRACK_NUM = "Benutzerdefinierte Titelnummer hinzufügen"
    SETTING_AUDIO_QUALITY = "Tonqualität"
    SETTING_VIDEO_QUALITY = "Videoqualität"
    SETTING_CHECK_EXIST = "Existenz überprüfen"
    SETTING_ARTIST_BEFORE_TITLE = "Künstlername vor Songtitel"
    SETTING_ALBUMID_BEFORE_FOLDER = "Id vor Album-Ordner"
    SETTING_INCLUDE_EP = "Einschließlich single&ep"
    SETTING_SAVE_COVERS = "Cover speichern"
    SETTING_LANGUAGE = "Sprache"
    SETTING_USE_PLAYLIST_FOLDER = "Playlist-Ordner verwenden"
    SETTING_MULITHREAD_DOWNLOAD = "Multi-Thread-Download"
    SETTING_ALBUM_FOLDER_FORMAT = "Album folder format"
    SETTING_TRACK_FILE_FORMAT = "Track file format"
    SETTING_SHOW_PROGRESS = "Show progress"

    CHOICE = "AUSWAHL"
    FUNCTION = "FUNKTION"
    CHOICE_ENTER = "Mit"
    CHOICE_ENTER_URLID = "'Url/ID' eingeben:"
    CHOICE_EXIT = "Beenden"
    CHOICE_LOGIN = "Check AccessToken"
    CHOICE_SETTINGS = "Einstellungen"
    CHOICE_SET_ACCESS_TOKEN = "AccessToken setzen"
    CHOICE_DOWNLOAD_BY_URL = "Herunterladen per URL oder ID"
    CHOICE_LOGOUT = "Logout"

    PRINT_ERR = "[ERR]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[SUCCESS]"

    PRINT_ENTER_CHOICE = "Auswahl:"
    PRINT_LATEST_VERSION = "Neueste Version:"
    #PRINT_USERNAME = "Benutzername:"
    #PRINT_PASSWORD = "Passwort:"
    
    CHANGE_START_SETTINGS = "Einstellungen starten ('0'-Zurück,'1'-Ja):"
    CHANGE_DOWNLOAD_PATH = "Download Pfad ('0' nicht ändern):"
    CHANGE_AUDIO_QUALITY = "Tonqualität ('0'-Normal,'1'-Hoch,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Videoqualität ('0'-1080,'1'-720,'2'-480,'3'-360):"
    CHANGE_ONLYM4A = "mp4 in m4a konvertieren ('0'-Nein,'1'-Ja):"
    CHANGE_ADD_EXPLICIT_TAG = "Explicit Tag zum Dateiname hinzufügen ('0'-Nein,'1'-Ja):"
    CHANGE_ADD_HYPHEN = "Verwende Bindestriche statt Leerzeichen im Dateiname ('0'-Nein,'1'-Ja):"
    CHANGE_ADD_YEAR = "Jahr zu Album-Ordnernamen hinzufügen ('0'-Nein,'1'-Ja):"
    CHANGE_USE_TRACK_NUM = "Titelnummer vor Dateinamen hinzufügen ('0'-Nein,'1'-Ja):"
    CHANGE_CHECK_EXIST = "Vor dem Download überprüfen, ob die Datei existiert ('0'-Nein,'1'-Ja):"
    CHANGE_ARTIST_BEFORE_TITLE = "Künstlername vor den Songtitel hinzufügen ('0'-Nein,'1'-Ja):"
    CHANGE_INCLUDE_EP = "Singles und EPs beim Download von Alben eines Künstlers einbeziehen ('0'-Nein,'1'-Ja):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "ID vor Album-Ordner hinzufügen ('0'-Nein,'1'-Ja):"
    CHANGE_SAVE_COVERS = "Cover speichern ('0'-Nein,'1'-Ja):"
    CHANGE_LANGUAGE = "Sprache auswählen"
    CHANGE_ALBUM_FOLDER_FORMAT = "Album folder format('0' not modify):"
    CHANGE_TRACK_FILE_FORMAT = "Track file format('0' not modify):"
    CHANGE_SHOW_PROGRESS = "Show progress('0'-No,'1'-Yes):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Starting login process..."
    AUTH_LOGIN_CODE = "Your login code is {}"
    AUTH_NEXT_STEP = "Go to {} within the next {} to complete setup."
    AUTH_WAITING = "Waiting for authorization..."
    AUTH_TIMEOUT = "Operation timed out."
    
    MSG_VALID_ACCESSTOKEN = "AccessToken good for {}."
    MSG_INVAILD_ACCESSTOKEN = "Expired AccessToken. Attempting to refresh it."
    MSG_PATH_ERR = "Path is error!"
    MSG_INPUT_ERR = "Input error!"

    MODEL_ALBUM_PROPERTY = "ALBUM-PROPERTY"
    MODEL_TRACK_PROPERTY = "TRACK-PROPERTY"
    MODEL_VIDEO_PROPERTY = "VIDEO-PROPERTY"
    MODEL_ARTIST_PROPERTY = "ARTIST-PROPERTY"
    MODEL_PLAYLIST_PROPERTY = "PLAYLIST-PROPERTY"

    MODEL_TITLE = 'Titel'
    MODEL_TRACK_NUMBER = 'Titelnummer'
    MODEL_VIDEO_NUMBER = 'Videonummer'
    MODEL_RELEASE_DATE = 'Veröffentlichungsdatum'
    MODEL_VERSION = 'Version'
    MODEL_EXPLICIT = 'Explicit'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Name'
    MODEL_TYPE = 'Typ'
