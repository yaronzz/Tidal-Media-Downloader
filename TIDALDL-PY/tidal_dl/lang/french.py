#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   french.py
@Time    :   2020/10/25
@Authors :   flamme-demon & joyel24
@Version :   0.3
@Contact :   
@Desc    :   
'''


class LangFrench(object):
    SETTING = "RÉGLAGES"
    VALUE = "VALEUR"
    SETTING_DOWNLOAD_PATH = "Emplacement des téléchargements"
    SETTING_ONLY_M4A = "Convertir mp4 en m4a"
    SETTING_ADD_EXPLICIT_TAG = "Ajout du tag Explicit - Dossier"
    SETTING_ADD_HYPHEN = "Ajouter un trait d'union"
    SETTING_ADD_YEAR = "Ajouter l'année avant le nom de l'album - Dossier"
    SETTING_USE_TRACK_NUM = "Ajouter le numéro de piste de l'album"
    SETTING_AUDIO_QUALITY = "Qualité Audio"
    SETTING_VIDEO_QUALITY = "Qualité Video"
    SETTING_CHECK_EXIST = "Vérifier l'existence"
    SETTING_ARTIST_BEFORE_TITLE = "Nom de l'artiste avant le titre du morceau - Fichier"
    SETTING_ALBUMID_BEFORE_FOLDER = "Id avant le nom d'album - Dossier"
    SETTING_INCLUDE_EP = "Inclure les singles & EPs"
    SETTING_SAVE_COVERS = "Sauvegarder les couvertures"
    SETTING_LANGUAGE = "Langue"
    SETTING_USE_PLAYLIST_FOLDER = "Utiliser dossier de playlist"
    SETTING_MULITHREAD_DOWNLOAD = "Téléchargement multithread"
    SETTING_ALBUM_FOLDER_FORMAT = "Format du dossier d'album"
    SETTING_PLAYLIST_FOLDER_FORMAT = "Playlist folder format"
    SETTING_TRACK_FILE_FORMAT = "Format du fichier de tracklist"
    SETTING_VIDEO_FILE_FORMAT = "Video file format"
    SETTING_SHOW_PROGRESS = "Afficher la Progression"
    SETTING_SHOW_TRACKINFO = "Afficher les information de la musique"
    SETTING_SAVE_ALBUMINFO = "Enregistrer AlbumInfo.txt"
    SETTING_DOWNLOAD_VIDEOS = "Download videos"
    SETTING_ADD_LYRICS = "Inclure les paroles"
    SETTING_LYRICS_SERVER_PROXY = "Proxy du serveur de paroles"
    SETTING_ADD_LRC_FILE = "Enregistrer les paroles synchronisées (fichier .lrc)"
    SETTING_PATH = "Emplacement des paramètres"
    SETTING_APIKEY = "Prise en charge de la clé API"
    SETTING_ADD_TYPE_FOLDER = "Ajouter un dossier de type"
    SETTING_DOWNLOAD_DELAY = "Use Download Delay"
    SETTING_LISTENER_ENABLED = "Listener mode enabled"
    SETTING_LISTENER_PORT = "Listener port"
    SETTING_LISTENER_SECRET = "Listener secret"

    CHOICE = "CHOIX"
    FUNCTION = "FONCTION"
    CHOICE_ENTER = "Saisir"
    CHOICE_ENTER_URLID = "Saisir 'Url/ID':"
    CHOICE_EXIT = "Quitter"
    CHOICE_LOGIN = "Vérifier le token d'accès"
    CHOICE_SETTINGS = "Réglages"
    CHOICE_SET_ACCESS_TOKEN = "Définir le jeton d'accès"
    CHOICE_DOWNLOAD_BY_URL = "Téléchargement par url ou id"
    CHOICE_LOGOUT = "Déconnexion"
    CHOICE_APIKEY = "Choisir la clé d'API"
    CHOICE_PKCE_LOGIN = "Login via PKCE"
    CHOICE_LISTENER = "Start listener mode"

    PRINT_ERR = "[ERR]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[SUCCES]"

    PRINT_ENTER_CHOICE = "Saisir le choix:"
    PRINT_LATEST_VERSION = "Dernière version:"
    # PRINT_USERNAME = "Utilisateur:"
    # PRINT_PASSWORD = "Mot de passe:"

    CHANGE_START_SETTINGS = "Commencer les réglages ('0'-Retour,'1'-Oui):"
    CHANGE_DOWNLOAD_PATH = "Emplacement des téléchargements('0' ne pas modifier):"
    CHANGE_AUDIO_QUALITY = "Qualité audio('0'-Normal,'1'-High,'2'-HiFi,'3'-Master,'4'-Max):"
    CHANGE_VIDEO_QUALITY = "Qualité Video(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Convertir mp4 en m4a('0'-Non,'1'-Oui):"
    CHANGE_ADD_EXPLICIT_TAG = "Ajout du tag Explicit - Fichier('0'-Non,'1'-Oui):"
    CHANGE_ADD_HYPHEN = "Utilisez des traits d'union au lieu d'espaces dans les noms de fichiers('0'-Non,'1'-Oui):"
    CHANGE_ADD_YEAR = "Ajouter l'année aux noms des dossiers des albums('0'-Non,'1'-Oui):"
    CHANGE_USE_TRACK_NUM = "Ajouter le numéro de piste avant le nom des fichiers('0'-Non,'1'-Oui):"
    CHANGE_CHECK_EXIST = "Vérifier l'existence du fichier avant le téléchargement('0'-Non,'1'-Oui):"
    CHANGE_ARTIST_BEFORE_TITLE = "Ajouter le nom de l'artiste avant le titre de la piste('0'-Non,'1'-Oui):"
    CHANGE_INCLUDE_EP = "Inclure les singles et les EPs lors du téléchargement des albums d'un artiste('0'-Non,'1'-Oui):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Ajouter un identifiant avant le dossier album('0'-Non,'1'-Oui):"
    CHANGE_SAVE_COVERS = "Sauvegarder les couvertures('0'-Non,'1'-Oui):"
    CHANGE_LANGUAGE = "Sélectionnez une langue"
    CHANGE_ALBUM_FOLDER_FORMAT = "Format du dossier d'album('0' ne pas modifier):"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Playlist folder format('0'-not modify,'default'-to set default):"
    CHANGE_TRACK_FILE_FORMAT = "Format du fichier de tracklist('0' ne pas modifier):"
    CHANGE_VIDEO_FILE_FORMAT = "Video file format('0'-not modify,'default'-to set default):"
    CHANGE_SHOW_PROGRESS = "Afficher la progression('0'-Non,'1'-Oui):"
    CHANGE_SHOW_TRACKINFO = "Afficher les information de la piste ('0'-Non,'1'-Oui):"
    CHANGE_SAVE_ALBUM_INFO = "Enregistrer AlbumInfo.txt('0'-Non,'1'-Oui):"
    CHANGE_DOWNLOAD_VIDEOS = "Download videos (when downloading playlists, albums, mixes)('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Ajouter les paroles ('0'-Non,'1'-Oui):"
    CHANGE_LYRICS_SERVER_PROXY = "Proxy du serveur de paroles('0'-not modify):"
    CHANGE_ADD_LRC_FILE = "Enregistrer les paroles synchronisées (fichier.lrc) ('0'-Non,'1'-Oui):"
    CHANGE_ADD_TYPE_FOLDER = "Ajouter un dossier de type,Ex: Album/Video/Playlist('0'-Non,'1'-Oui):"
    CHANGE_MULITHREAD_DOWNLOAD = "Multi thread download('0'-Non,'1'-Oui):"
    CHANGE_USE_DOWNLOAD_DELAY = "Use Download Delay('0'-No,'1'-Yes):"
    CHANGE_ENABLE_LISTENER = "Enable listener mode('0'-No,'1'-Yes):"
    CHANGE_LISTENER_SECRET = "Listener secret('0'-not modify):"
    CHANGE_LISTENER_PORT = "Listener port('0'-not modify):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Démarrage du processus de connexion..."
    AUTH_LOGIN_CODE = "Votre code de connection est le suivant: {}"
    AUTH_NEXT_STEP = "Allez à {} avant {} pour finir la configuration."
    AUTH_WAITING = "En attente d'autorisation..."
    AUTH_TIMEOUT = "Temps écoulé."

    MSG_VALID_ACCESSTOKEN = "Token d'accès valable {}."
    MSG_INVALID_ACCESSTOKEN = "Token d'accès expiré. Tentative de renouvellement automatique."
    MSG_PATH_ERR = "Erreur du chemin d'accès"
    MSG_INPUT_ERR = "Erreur de saisie !"

    MODEL_ALBUM_PROPERTY = "PROPRIETES-ALBUM"
    MODEL_TRACK_PROPERTY = "PROPRIETES-PISTES-AUDIO"
    MODEL_VIDEO_PROPERTY = "PROPRIETES-VIDEO"
    MODEL_ARTIST_PROPERTY = "PROPRIETES-ARTISTE"
    MODEL_PLAYLIST_PROPERTY = "PROPERTES-PLAYLIST"

    MODEL_TITLE = 'Titre'
    MODEL_TRACK_NUMBER = 'Numéro de piste'
    MODEL_VIDEO_NUMBER = 'Numéro de la vidéo'
    MODEL_RELEASE_DATE = 'Date de publication'
    MODEL_VERSION = 'Version'
    MODEL_EXPLICIT = 'Explicit'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Nom'
    MODEL_TYPE = 'Type'
