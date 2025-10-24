#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   dutch.py
@Time    :   2022/03/01
@Author  :   bladeoner
@Version :   1.0
@Contact :
@Desc    :   
'''


class LangDutch(object):
    SETTING = "INSTELLINGEN"
    VALUE = "WAARDE"
    SETTING_DOWNLOAD_PATH = "Download pad"
    SETTING_ONLY_M4A = "mp4 naar m4a converteren"
    SETTING_ADD_EXPLICIT_TAG = "Expliciete tag toevoegen"
    SETTING_ADD_HYPHEN = "Koppelteken toevoegen"
    SETTING_ADD_YEAR = "Jaar voor albummap toevoegen"
    SETTING_USE_TRACK_NUM = "Tracknummer gebruiker toevoegen"
    SETTING_AUDIO_QUALITY = "Audiokwaliteit"
    SETTING_VIDEO_QUALITY = "Videokwaliteit"
    SETTING_CHECK_EXIST = "Controleer of al bestaat"
    SETTING_ARTIST_BEFORE_TITLE = "Artiestnaam voor tracktitel"
    SETTING_ALBUMID_BEFORE_FOLDER = "ID voor albummap"
    SETTING_INCLUDE_EP = "Inclusief singles en EP's"
    SETTING_SAVE_COVERS = "Bewaar covers"
    SETTING_LANGUAGE = "Taal"
    SETTING_USE_PLAYLIST_FOLDER = "Afspeellijst gebruiken"
    SETTING_MULITHREAD_DOWNLOAD = "Downloaden met meerdere threads"
    SETTING_ALBUM_FOLDER_FORMAT = "Indeling albummap"
    SETTING_PLAYLIST_FOLDER_FORMAT = "Playlist folder format"
    SETTING_TRACK_FILE_FORMAT = "Bestandsindeling bijhouden"
    SETTING_VIDEO_FILE_FORMAT = "Videobestandsindeling"
    SETTING_SHOW_PROGRESS = "Toon voortgang"
    SETTING_SHOW_TRACKINFO = "Toon trackinfo"
    SETTING_SAVE_ALBUMINFO = "AlbumInfo.txt opslaan"
    SETTING_DOWNLOAD_VIDEOS = "Download videos"
    SETTING_ADD_LYRICS = "Songtekst toevoegen"
    SETTING_LYRICS_SERVER_PROXY = "Tekst server proxy"
    SETTING_ADD_LRC_FILE = "Getimede songteksten opslaan (.lrc-bestand)"
    SETTING_PATH = "Instellingen pad"
    SETTING_APIKEY = "APIKey-ondersteuning"
    SETTING_ADD_TYPE_FOLDER = "Typemap toevoegen"
    SETTING_DOWNLOAD_DELAY = "Use Download Delay"
    SETTING_LISTENER_ENABLED = "Listener mode enabled"
    SETTING_LISTENER_PORT = "Listener port"
    SETTING_LISTENER_SECRET = "Listener secret"

    CHOICE = "KEUZE"
    FUNCTION = "FUNCTIE"
    CHOICE_ENTER = "Voer in"
    CHOICE_ENTER_URLID = "Vul 'Url/ID' in:"
    CHOICE_EXIT = "Verlaten"
    CHOICE_LOGIN = "Toegangstoken controleren"
    CHOICE_SETTINGS = "Instellingen"
    CHOICE_SET_ACCESS_TOKEN = "Toegangstoken instellen"
    CHOICE_DOWNLOAD_BY_URL = "Downloaden via url of ID"
    CHOICE_LOGOUT = "Uitloggen"
    CHOICE_APIKEY = "Selecteer APIKey"
    CHOICE_PKCE_LOGIN = "Login via PKCE"
    CHOICE_LISTENER = "Start listener mode"

    PRINT_ERR = "[FOUT]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[SUCCESS]"

    PRINT_ENTER_CHOICE = "Voer keuze in:"
    PRINT_LATEST_VERSION = "Laatste versie:"
    # PRINT_USERNAME = "gebruikersnaam:"
    # PRINT_PASSWORD = "wachtwoord:"

    CHANGE_START_SETTINGS = "Start instellingen('0'-Terugkeren,'1'-Ja):"
    CHANGE_DOWNLOAD_PATH = "Downloadpad('0'-niet wijzigen):"
    CHANGE_AUDIO_QUALITY = "Audiokwaliteit('0'-Normaal,'1'-Hoog,'2'-HiFi,'3'-Master,'4'-Max):"
    CHANGE_VIDEO_QUALITY = "Videokwaliteit (1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Converteer mp4 naar m4a('0'-Nee,'1'-Ja):"
    CHANGE_ADD_EXPLICIT_TAG = "Expliciete tag toevoegen aan bestandsnamen('0'-Nee,'1'-Ja):"
    CHANGE_ADD_HYPHEN = "Gebruik koppeltekens in plaats van spaties in bestandsnamen ('0'-Nee,'1'-Ja):"
    CHANGE_ADD_YEAR = "Jaar toevoegen aan albummapnamen ('0'-Nee,'1'-Ja):"
    CHANGE_USE_TRACK_NUM = "Voeg tracknummer toe voor bestandsnamen ('0'-Nee,'1'-Ja):"
    CHANGE_CHECK_EXIST = "Controleer het bestaande bestand voordat u de track downloadt('0'-Nee,'1'-Ja):"
    CHANGE_ARTIST_BEFORE_TITLE = "Voeg artiestnaam toe voor de tracktitel ('0'-Nee,'1'-Ja):"
    CHANGE_INCLUDE_EP = "Voeg singles en EP's toe bij het downloaden van de albums van een artiest('0'-Nee,'1'-Ja):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "ID toevoegen voor albummap ('0'-Nee,'1'-Ja):"
    CHANGE_SAVE_COVERS = "Covers opslaan('0'-Nee,'1'-Ja):"
    CHANGE_LANGUAGE = "Selecteer taal"
    CHANGE_ALBUM_FOLDER_FORMAT = "Albummapindeling ('0'-niet wijzigen,'default'-om standaard in te stellen):"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Afspeellijstmapindeling format('0'-niet wijzigen,'default'-om standaard in te stellen):"
    CHANGE_TRACK_FILE_FORMAT = "Bestandsformaat bijhouden ('0'-niet wijzigen,'default'-om standaard in te stellen):"
    CHANGE_VIDEO_FILE_FORMAT = "Videobestandsindeling('0'-niet wijzigen,'default'-om standaard in te stellen):"
    CHANGE_SHOW_PROGRESS = "Voortgang weergeven('0'-Nee,'1'-Ja):"
    CHANGE_SHOW_TRACKINFO = "Toon trackinfo('0'-Nee,'1'-Ja):"
    CHANGE_SAVE_ALBUM_INFO = "Bewaar AlbumInfo.txt('0'-Nee,'1'-Ja):"
    CHANGE_DOWNLOAD_VIDEOS = "Download videos (when downloading playlists, albums, mixes)('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Songtekst toevoegen('0'-Nee,'1'-Ja):"
    CHANGE_LYRICS_SERVER_PROXY = "Songtekst proxyserver('0'-niet wijzigen):"
    CHANGE_ADD_LRC_FILE = "Sla getimede songtekst .lrc-bestand op ('0'-Nee,'1'-Ja):"
    CHANGE_ADD_TYPE_FOLDER = "Type-map toevoegen, bijv. Album/Video/Playlist('0'-Nee,'1'-Ja):"
    CHANGE_MULITHREAD_DOWNLOAD = "Multi thread download('0'-No,'1'-Yes):"
    CHANGE_USE_DOWNLOAD_DELAY = "Use Download Delay('0'-No,'1'-Yes):"
    CHANGE_ENABLE_LISTENER = "Enable listener mode('0'-No,'1'-Yes):"
    CHANGE_LISTENER_SECRET = "Listener secret('0'-not modify):"
    CHANGE_LISTENER_PORT = "Listener port('0'-not modify):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Inlogproces starten..."
    AUTH_LOGIN_CODE = "Uw inlogcode is {}"
    AUTH_NEXT_STEP = "Ga naar {} in de volgende {} om de installatie te voltooien."
    AUTH_WAITING = "Wachten op toestemming..."
    AUTH_TIMEOUT = "Operatie time-out."

    MSG_VALID_ACCESSTOKEN = "Toegangstoken goed voor {}."
    MSG_INVALID_ACCESSTOKEN = "Verlopen AccessToken. Poging om het te vernieuwen."
    MSG_PATH_ERR = "Pad is incorrect!"
    MSG_INPUT_ERR = "Invoerfout!"

    MODEL_ALBUM_PROPERTY = "ALBUM-EIGENSCHAP"
    MODEL_TRACK_PROPERTY = "TRACK-EIGENSCHAP"
    MODEL_VIDEO_PROPERTY = "VIDEO-EIGENSCHAP"
    MODEL_ARTIST_PROPERTY = "ARTIEST-EIGENSCHAP"
    MODEL_PLAYLIST_PROPERTY = "AFSPEELLIJST-EIGENSCHAP"

    MODEL_TITLE = 'Titel'
    MODEL_TRACK_NUMBER = 'Tracknummer'
    MODEL_VIDEO_NUMBER = 'Videonummer'
    MODEL_RELEASE_DATE = 'Publicatiedatum'
    MODEL_VERSION = 'Versie'
    MODEL_EXPLICIT = 'Expliciet'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Naam'
    MODEL_TYPE = 'Type'
