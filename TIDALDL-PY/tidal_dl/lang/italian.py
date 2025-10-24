#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   italian.py
@Time    :   2020/08/20
@Author  :   Normando
@Version :   1.0
@Contact :   normando@me.com
@Desc    :
'''


class LangItalian(object):
    SETTING = "IMPOSTAZIONI"
    VALUE = "VALORE"
    SETTING_DOWNLOAD_PATH = "Percorso Download"
    SETTING_ONLY_M4A = "Convertire mp4 in m4a"
    SETTING_ADD_EXPLICIT_TAG = "Aggiungere tag 'Contenuto esplicito'"
    SETTING_ADD_HYPHEN = "Aggiungere trattino"
    SETTING_ADD_YEAR = "Aggiungere anno nella cartella album"
    SETTING_USE_TRACK_NUM = "Aggiungere numero traccia utente"
    SETTING_AUDIO_QUALITY = "Qualità Audio"
    SETTING_VIDEO_QUALITY = "Video Video"
    SETTING_CHECK_EXIST = "Controlla esistenza"
    SETTING_ARTIST_BEFORE_TITLE = "Nome artista prima del titolo della traccia"
    SETTING_ALBUMID_BEFORE_FOLDER = "Numero Id nell cartella album"
    SETTING_INCLUDE_EP = "Includere singolo&ep"
    SETTING_SAVE_COVERS = "Salva copertine"
    SETTING_LANGUAGE = "Lingua"
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

    CHOICE = "SCELTA"
    FUNCTION = "FUNZIONE"
    CHOICE_ENTER = "Inserire"
    CHOICE_ENTER_URLID = "Inserire 'Url/ID':"
    CHOICE_EXIT = "Uscita"
    CHOICE_LOGIN = "Check AccessToken"
    CHOICE_SETTINGS = "Impostazioni"
    CHOICE_SET_ACCESS_TOKEN = "Imposta AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Scarica per URL o Id"
    CHOICE_LOGOUT = "Logout"
    CHOICE_APIKEY = "Select APIKey"
    CHOICE_PKCE_LOGIN = "Login via PKCE"
    CHOICE_LISTENER = "Start listener mode"

    PRINT_ERR = "[ERR]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[SUCCESSO]"

    PRINT_ENTER_CHOICE = "Inserire scelta:"
    PRINT_LATEST_VERSION = "Ultima versione:"
    # PRINT_USERNAME = "username:"
    # PRINT_PASSWORD = "password:"

    CHANGE_START_SETTINGS = "Impostazioni all'avvio ('0'-Ritorna,'1'-Sì):"
    CHANGE_DOWNLOAD_PATH = "Percorso Download ('0' non modificare):"
    CHANGE_AUDIO_QUALITY = "Qualità Audio ('0'-Normale, '1'-Alta, '2'-HiFi, '3'-Master,'4'-Max):"
    CHANGE_VIDEO_QUALITY = "Qualità Video (1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Convertire mp4 in m4a ('0'-No,'1'-):"
    CHANGE_ADD_EXPLICIT_TAG = "Aggiungi tag 'Contenuto Esplicito' ai nomi dei file ('0'-No,'1'-Sì):"
    CHANGE_ADD_HYPHEN = "Usare trattini al posto degli spazi nei nomi dei file ('0'-No,'1'-Sì):"
    CHANGE_ADD_YEAR = "Aggiungere l'anno al nome della cartella dell'album ('0'-No,'1'-Sì):"
    CHANGE_USE_TRACK_NUM = "Aggiungere il numero traccia prima del nome dei file ('0'-No,'1'-Sì):"
    CHANGE_CHECK_EXIST = "Controllare se il file esiste prima di scaricare la traccia ('0'-No,'1'-Sì):"
    CHANGE_ARTIST_BEFORE_TITLE = "Aggiungere il nome dell'artista prima del titolo della traccia ('0'-No,'1'-Sì):"
    CHANGE_INCLUDE_EP = "Includere singoli e EP quando si scaricano gli album di un artista ('0'-No,'1'-Sì):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Aggiungere ID prima del nome della cartella per l'album ('0'-No,'1'-Sì):"
    CHANGE_SAVE_COVERS = "Salve copertine ('0'-No,'1'-Sì):"
    CHANGE_LANGUAGE = "Selezionare lingua"
    CHANGE_ALBUM_FOLDER_FORMAT = "Album folder format('0' not modify,'default'-to set default):"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Playlist folder format('0'-not modify,'default'-to set default):"
    CHANGE_TRACK_FILE_FORMAT = "Track file format('0' not modify,'default'-to set default):"
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
    MSG_PATH_ERR = "Percorso errato!"
    MSG_INPUT_ERR = "Inserimento errato!"

    MODEL_ALBUM_PROPERTY = "PROPRIETÀ-ALBUM"
    MODEL_TRACK_PROPERTY = "PROPRIETÀ-TRACCIA"
    MODEL_VIDEO_PROPERTY = "PROPRIETÀ-VIDEO"
    MODEL_ARTIST_PROPERTY = "PROPRIETÀ-ARTISTA"
    MODEL_PLAYLIST_PROPERTY = "PROPRIETÀ-PLAYLIST"

    MODEL_TITLE = 'Titolo'
    MODEL_TRACK_NUMBER = 'Numero Traccia'
    MODEL_VIDEO_NUMBER = 'Numero Video'
    MODEL_RELEASE_DATE = 'Data uscita'
    MODEL_VERSION = 'Versione'
    MODEL_EXPLICIT = 'Contenuto Esplicito'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Nome'
    MODEL_TYPE = 'Tipo'
