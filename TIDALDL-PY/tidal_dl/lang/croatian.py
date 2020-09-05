 #!/usr/bin/env python

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

    CHOICE = "ODABIR"
    FUNCTION = "FUNKCIJA"
    CHOICE_ENTER = "Ulaz"
    CHOICE_ENTER_URLID = "Unesi 'Url/ID':"
    CHOICE_EXIT = "Izlaz"
    CHOICE_LOGIN = "Prijava"
    CHOICE_SETTINGS = "Postavke"
    CHOICE_SET_ACCESS_TOKEN = "Postavi AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Preuzmi po url-u ili ID-u"

    PRINT_ERR = "[ERR]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[USPIJESNO]"

    PRINT_ENTER_CHOICE = "Unesi odabir:"
    PRINT_LATEST_VERSION = "Posljednja verzija:"
    PRINT_USERNAME = "korisnik:"
    PRINT_PASSWORD = "lozinka:"
    
    CHANGE_START_SETTINGS = "Pokreni postavke (0'-Izlaz,'1'-Da):"
    CHANGE_DOWNLOAD_PATH = "Putanja preuzimanja('0' ne mijenjaj):"
    CHANGE_AUDIO_QUALITY = "Kvaliteta zvuka('0'-Normalna,'1'-Visoka,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Kvaliteta videozapisa('0'-1080,'1'-720,'2'-480,'3'-360):"
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

    MSG_INVAILD_ACCESSTOKEN = "Nevazeci AccessToken! Molim da ga resetirate."
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
