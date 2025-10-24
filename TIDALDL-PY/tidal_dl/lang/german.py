#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   german.py
@Time    :   2022/11/8
@Authors :   Sematre, MineClashTV, Click1701
@Version :   1.1
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
    SETTING_ALBUMID_BEFORE_FOLDER = "ID vor Album-Ordner"
    SETTING_INCLUDE_EP = "Singles & EPs einschließen"
    SETTING_SAVE_COVERS = "Cover speichern"
    SETTING_LANGUAGE = "Sprache"
    SETTING_USE_PLAYLIST_FOLDER = "Playlist-Ordner verwenden"
    SETTING_MULITHREAD_DOWNLOAD = "Multi-Thread Download"
    SETTING_ALBUM_FOLDER_FORMAT = "Album-Ordnerformat"
    SETTING_PLAYLIST_FOLDER_FORMAT = "Playlist-Ordnerformat"
    SETTING_TRACK_FILE_FORMAT = "Track-Dateiformat"
    SETTING_VIDEO_FILE_FORMAT = "Video-Dateiformat"
    SETTING_SHOW_PROGRESS = "Fortschritt anzeigen"
    SETTING_SHOW_TRACKINFO = "Titelinformationen anzeigen"
    SETTING_SAVE_ALBUMINFO = "AlbumInfo.txt speichern"
    SETTING_DOWNLOAD_VIDEOS = "Download videos"
    SETTING_ADD_LYRICS = "Songtexte hinzufügen"
    SETTING_LYRICS_SERVER_PROXY = "Songtext Proxy-Server"
    SETTING_ADD_LRC_FILE = "Songtext mit Zeitcode speichern (.lrc Datei)"
    SETTING_PATH = "Speicherort der Einstellungen"
    SETTING_APIKEY = "APIKey Unterstützung"
    SETTING_ADD_TYPE_FOLDER = "Unterordner für jede Kategorie erstellen"
    SETTING_DOWNLOAD_DELAY = "Downloads zeitverzögert starten"
    SETTING_LISTENER_ENABLED = "Listener mode enabled"
    SETTING_LISTENER_PORT = "Listener port"
    SETTING_LISTENER_SECRET = "Listener secret"

    CHOICE = "AUSWAHL"
    FUNCTION = "FUNKTION"
    CHOICE_ENTER = "Mit"
    CHOICE_ENTER_URLID = "'Url/ID' eingeben:"
    CHOICE_EXIT = "Beenden"
    CHOICE_LOGIN = "AccessToken überprüfen"
    CHOICE_SETTINGS = "Einstellungen"
    CHOICE_SET_ACCESS_TOKEN = "AccessToken setzen"
    CHOICE_DOWNLOAD_BY_URL = "Download per URL oder ID"
    CHOICE_LOGOUT = "Ausloggen"
    CHOICE_APIKEY = "APIKey Auswahl"
    CHOICE_PKCE_LOGIN = "Login via PKCE"
    CHOICE_LISTENER = "Start listener mode"
    CHOICE_LISTENER = "Start listener mode"

    PRINT_ERR = "[FEHLER]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[ERFOLG]"

    PRINT_ENTER_CHOICE = "Auswahl:"
    PRINT_LATEST_VERSION = "Neueste Version:"
    # PRINT_USERNAME = "Benutzername:"
    # PRINT_PASSWORD = "Passwort:"

    CHANGE_START_SETTINGS = "Einstellungen starten ('0'-Zurück, '1'-Ja):"
    CHANGE_DOWNLOAD_PATH = "Downloadpfad ('0' nicht ändern):"
    CHANGE_AUDIO_QUALITY = "Tonqualität ('0'-Normal, '1'-Hoch, '2'-HiFi, '3'-Master,'4'-Max):"
    CHANGE_VIDEO_QUALITY = "Videoqualität (1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "mp4 in m4a konvertieren ('0'-Nein, '1'-Ja):"
    CHANGE_ADD_EXPLICIT_TAG = "Explicit Tag zum Dateiname hinzufügen ('0'-Nein, '1'-Ja):"
    CHANGE_ADD_HYPHEN = "Im Dateinamen Bindestriche statt Leerzeichen verwenden ('0'-Nein, '1'-Ja):"
    CHANGE_ADD_YEAR = "Jahr zu Album-Ordnernamen hinzufügen ('0'-Nein, '1'-Ja):"
    CHANGE_USE_TRACK_NUM = "Titelnummer vor Dateinamen hinzufügen ('0'-Nein, '1'-Ja):"
    CHANGE_CHECK_EXIST = "Vor dem Download überprüfen, ob die Datei existiert ('0'-Nein, '1'-Ja):"
    CHANGE_ARTIST_BEFORE_TITLE = "Künstlername vor den Songtitel hinzufügen ('0'-Nein, '1'-Ja):"
    CHANGE_INCLUDE_EP = "Singles und EPs beim Download von Alben eines Künstlers einbeziehen ('0'-Nein, '1'-Ja):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "ID vor Album-Ordner hinzufügen ('0'-Nein, '1'-Ja):"
    CHANGE_SAVE_COVERS = "Cover speichern ('0'-Nein, '1'-Ja):"
    CHANGE_LANGUAGE = "Sprache auswählen"
    CHANGE_ALBUM_FOLDER_FORMAT = "Album-Ordnerformat ('0' überspringen):"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Playlist Ordner-Format ('0'-nicht ändern, 'default'-für Standard):"
    CHANGE_TRACK_FILE_FORMAT = "Track-Dateiformat ('0' überspringen):"
    CHANGE_VIDEO_FILE_FORMAT = "Video-Dateiformat ('0'-nicht ändern, 'default'-für Standard):"
    CHANGE_SHOW_PROGRESS = "Fortschritt anzeigen ('0'-Nein, '1'-Ja):"
    CHANGE_SHOW_TRACKINFO = "Song-Informationen anzeigen ('0'-Nein, '1'-Ja):"
    CHANGE_SAVE_ALBUM_INFO = "AlbumInfo.txt speichern ('0'-Nein, '1'-Ja):"
    CHANGE_DOWNLOAD_VIDEOS = "Download videos (when downloading playlists, albums, mixes)('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Songtexte hinzufügen ('0'-No, '1'-Yes):"
    CHANGE_LYRICS_SERVER_PROXY = "Songtext Proxy-Server ('0'-not modify):"
    CHANGE_ADD_LRC_FILE = "Songtexte mit Zeitcode speichern (.lrc Datei) ('0'-Nein, '1'-Ja):"
    CHANGE_ADD_TYPE_FOLDER = "Unterordner für jede Kategorie erstellen, Z.B. Album/Video/Playlist('0'-Nein, '1'-Ja):"
    CHANGE_MULITHREAD_DOWNLOAD = "Multi-Thread Download('0'-Nein, '1'-Ja):"
    CHANGE_USE_DOWNLOAD_DELAY = "Downloads zeitverzögert starten ('0'-nein, '1'-ja):"
    CHANGE_ENABLE_LISTENER = "Enable listener mode('0'-No,'1'-Yes):"
    CHANGE_LISTENER_SECRET = "Listener secret('0'-not modify):"
    CHANGE_LISTENER_PORT = "Listener port('0'-not modify):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Starte Loginprozess..."
    AUTH_LOGIN_CODE = "Dein Logincode ist {}"
    AUTH_NEXT_STEP = "Gehe auf {} in den nächsten {} um das Setup abzuschließen."
    AUTH_WAITING = "Warte auf Autorisierung..."
    AUTH_TIMEOUT = "Zeitüberschreitung der Operation."

    MSG_VALID_ACCESSTOKEN = "AccessToken gültig für {}."
    MSG_INVALID_ACCESSTOKEN = "AccessToken abgelaufen. Er muss erneuert werden."
    MSG_PATH_ERR = "Ungültiger Pfad!"
    MSG_INPUT_ERR = "Eingabefehler!"

    MODEL_ALBUM_PROPERTY = "ALBUM-EIGENSCHAFT"
    MODEL_TRACK_PROPERTY = "TRACK-EIGENSCHAFT"
    MODEL_VIDEO_PROPERTY = "VIDEO-EIGENSCHAFT"
    MODEL_ARTIST_PROPERTY = "KÜNSTLER-EIGENSCHAFT"
    MODEL_PLAYLIST_PROPERTY = "PLAYLIST-EIGENSCHAFT"

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
