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

    CHOICE = "Výběr"
    FUNCTION = "Funkce"
    CHOICE_ENTER = "Enter"
    CHOICE_ENTER_URLID = "Vložit 'Url/ID':"
    CHOICE_EXIT = "Ukončit"
    CHOICE_LOGIN = "Přihlášení"
    CHOICE_SETTINGS = "Nastavení"
    CHOICE_SET_ACCESS_TOKEN = "Nastavit přístupový token"
    CHOICE_DOWNLOAD_BY_URL = "Stáhnout buď url nebo id"

    PRINT_ERR = "[Error]"
    PRINT_INFO = "[Info]"
    PRINT_SUCCESS = "[Staženo]"

    PRINT_ENTER_CHOICE = "Zvolit volbu:"
    PRINT_LATEST_VERSION = "Nejnovější verze:"
    PRINT_USERNAME = "přihlašovací jméno:"
    PRINT_PASSWORD = "heslo"
    
    CHANGE_START_SETTINGS = "Start settings('0'-Zpět,'1'-Ano):"
    CHANGE_DOWNLOAD_PATH = "Cesta stažení('0' not modify):"
    CHANGE_AUDIO_QUALITY = "Kvalita hudby('0'-Normal,'1'-High,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Kvalita videa('0'-1080,'1'-720,'2'-480,'3'-360):"
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

    MSG_INVAILD_ACCESSTOKEN = "Neplatný přístupový token! Prosím restartujte aplikaci."
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
