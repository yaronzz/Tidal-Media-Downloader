#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   french.py
@Time    :   2020/09/07
@Author  :   flamme-demon
@Version :   0.2
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
    SETTING_ADD_YEAR = "Ajouter l'année avant le nom de l'album - Dosser"
    SETTING_USE_TRACK_NUM = "Add user track number"
    SETTING_AUDIO_QUALITY = "Qualité Audio"
    SETTING_VIDEO_QUALITY = "Qualité Video"
    SETTING_CHECK_EXIST = "Vérifier l'existence"
    SETTING_ARTIST_BEFORE_TITLE = "Nom de l'artiste avant le titre du morceau - Fichier"
    SETTING_ALBUMID_BEFORE_FOLDER = "Id avant le nom d'album - Dossier"
    SETTING_INCLUDE_EP = "Inclure les single&ep"
    SETTING_SAVE_COVERS = "Sauvegarder les couvertures"
    SETTING_LANGUAGE = "Langue"
    SETTING_USE_PLAYLIST_FOLDER = "Use playlist folder"
    SETTING_MULITHREAD_DOWNLOAD = "Mulit thread download"
    SETTING_ALBUM_FOLDER_FORMAT = "Album folder format"
    SETTING_TRACK_FILE_FORMAT = "Track file format"

    CHOICE = "CHOIX"
    FUNCTION = "FONCTION"
    CHOICE_ENTER = "Saisir"
    CHOICE_ENTER_URLID = "Saisir 'Url/ID':"
    CHOICE_EXIT = "Quitter"
    CHOICE_LOGIN = "Login"
    CHOICE_SETTINGS = "Réglages"
    CHOICE_SET_ACCESS_TOKEN = "Définir AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Téléchargement par url ou id"

    PRINT_ERR = "[ERR]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[SUCCESS]"

    PRINT_ENTER_CHOICE = "Saisir le choix:"
    PRINT_LATEST_VERSION = "Dernière version:"
    PRINT_USERNAME = "username:"
    PRINT_PASSWORD = "password:"
    
    CHANGE_START_SETTINGS = "Commencer les règlages ('0'-Retour,'1'-Oui):"
    CHANGE_DOWNLOAD_PATH = "Emplacement des téléchargements('0' ne pas modifier):"
    CHANGE_AUDIO_QUALITY = "Qualité audio('0'-Normal,'1'-High,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Qualité Video('0'-1080,'1'-720,'2'-480,'3'-360):"
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
    CHANGE_ALBUM_FOLDER_FORMAT = "Album folder format('0' not modify):"
    CHANGE_TRACK_FILE_FORMAT = "Track file format('0' not modify):"

    MSG_INVAILD_ACCESSTOKEN = "Jeton d'accès disponible ! Veuillez recommencer."
    MSG_PATH_ERR = "L'emplacement est faux"
    MSG_INPUT_ERR = "Erreur de saisie !"

    MODEL_ALBUM_PROPERTY = "ALBUM-PROPERTY"
    MODEL_TRACK_PROPERTY = "TRACK-PROPERTY"
    MODEL_VIDEO_PROPERTY = "VIDEO-PROPERTY"
    MODEL_ARTIST_PROPERTY = "ARTIST-PROPERTY"
    MODEL_PLAYLIST_PROPERTY = "PLAYLIST-PROPERTY"

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
