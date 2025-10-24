#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   czech.py
@Time    :   2022/11/13
@Author  :   Tomikk & Sweder
@Version :   1.2
@Contact :   justtomikk@gmail.com & djsweder@gmail.com
@Desc    :   
'''


class LangCzech(object):
    SETTING = "Nastavení"
    VALUE = "Hodnota"
    SETTING_DOWNLOAD_PATH = "Umístění staženého souboru"
    SETTING_ONLY_M4A = "Konvertovat mp4 na m4a"
    SETTING_ADD_EXPLICIT_TAG = "Přidat označení explicity"
    SETTING_ADD_HYPHEN = "Místo mezer použít pomlčky"
    SETTING_ADD_YEAR = "Přidat rok před jméno složky"
    SETTING_USE_TRACK_NUM = "Přidat číslo skladby"
    SETTING_AUDIO_QUALITY = "Kvalita hudby"
    SETTING_VIDEO_QUALITY = "Kvalita videa"
    SETTING_CHECK_EXIST = "Zkontrolovat existenci souboru"
    SETTING_ARTIST_BEFORE_TITLE = "Jméno interpreta před jménem skladby"
    SETTING_ALBUMID_BEFORE_FOLDER = "Id před složkou alba"
    SETTING_INCLUDE_EP = "Zahrnout singly & EP"
    SETTING_SAVE_COVERS = "Uložit obal alba"
    SETTING_LANGUAGE = "Změna jazyka"
    SETTING_USE_PLAYLIST_FOLDER = "Používat složku playlistu"
    SETTING_MULITHREAD_DOWNLOAD = "Stahování více vlákny"
    SETTING_ALBUM_FOLDER_FORMAT = "Formát názvu složky alba"
    SETTING_PLAYLIST_FOLDER_FORMAT = "Playlist folder format"
    SETTING_TRACK_FILE_FORMAT = "Formát názvu souboru skladby"
    SETTING_VIDEO_FILE_FORMAT = "Formát názvu souboru videa"
    SETTING_SHOW_PROGRESS = "Zobrazit indikátor stavu stahování"
    SETTING_SHOW_TRACKINFO = "Zobrazit informace o skladbě"
    SETTING_SAVE_ALBUMINFO = "Uložit soubor AlbumInfo.txt"
    SETTING_DOWNLOAD_VIDEOS = "Download videos"
    SETTING_ADD_LYRICS = "Přidat texty skladeb"
    SETTING_LYRICS_SERVER_PROXY = "Server proxy pro texty skladeb"
    SETTING_ADD_LRC_FILE = "Uložit slova skladby s časováním (soubor .lrc)"
    SETTING_PATH = "Cesta k souboru s nastavením"
    SETTING_APIKEY = "APIKey podporuje"
    SETTING_ADD_TYPE_FOLDER = "Složky dle typu obsahu"
    SETTING_DOWNLOAD_DELAY = "Stahovat s časovou prodlevou"
    SETTING_LISTENER_ENABLED = "Listener mode enabled"
    SETTING_LISTENER_PORT = "Listener port"
    SETTING_LISTENER_SECRET = "Listener secret"

    CHOICE = "Výběr"
    FUNCTION = "Funkce"
    CHOICE_ENTER = "Zvolit"
    CHOICE_ENTER_URLID = "Vložit 'Url/ID':"
    CHOICE_EXIT = "Ukončit"
    CHOICE_LOGIN = "Zkontrolovat přístupový token"
    CHOICE_SETTINGS = "Nastavení"
    CHOICE_SET_ACCESS_TOKEN = "Nastavit přístupový token"
    CHOICE_DOWNLOAD_BY_URL = "Stáhnout buď dle URL nebo ID"
    CHOICE_LOGOUT = "Odhlásit"
    CHOICE_APIKEY = "Vybrat APIKey"
    CHOICE_PKCE_LOGIN = "Login via PKCE"
    CHOICE_LISTENER = "Start listener mode"
    CHOICE_LISTENER = "Start listener mode"

    PRINT_ERR = "[Chyba]"
    PRINT_INFO = "[Info]"
    PRINT_SUCCESS = "[Staženo]"

    PRINT_ENTER_CHOICE = "Zvolit volbu:"
    PRINT_LATEST_VERSION = "Nejnovější verze:"
    # PRINT_USERNAME = "přihlašovací jméno:"
    # PRINT_PASSWORD = "heslo"

    CHANGE_START_SETTINGS = "Spustit nastavení ('0'-Zpět,'1'-Ano):"
    CHANGE_DOWNLOAD_PATH = "Umístění stažených souborů ('0' beze změny):"
    CHANGE_AUDIO_QUALITY = "Kvalita hudby ('0'-Normální,'1'-Vysoká,'2'-HiFi,'3'-Master,'4'-Max):"
    CHANGE_VIDEO_QUALITY = "Kvalita videa (1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Konvertovat mp4 na m4a ('0'-Ne,'1'-Ano):"
    CHANGE_ADD_EXPLICIT_TAG = "Přidat označení explicity k souborům ('0'-Ne,'1'-Ano):"
    CHANGE_ADD_HYPHEN = "V názvech souborů používat místo mezer pomlčky ('0'-Ne,'1'-Ano):"
    CHANGE_ADD_YEAR = "Přidat rok vydání do názvu složky ('0'-Ne,'1'-Ano):"
    CHANGE_USE_TRACK_NUM = "Přidat číslo skladby před název skladby ('0'-Ne,'1'-Ano):"
    CHANGE_CHECK_EXIST = "Zkontrolovat existenci souboru před stažením ('0'-Ne,'1'-Ano):"
    CHANGE_ARTIST_BEFORE_TITLE = "Přidat jméno interpreta před název skladby ('0'-Ne,'1'-Ano):"
    CHANGE_INCLUDE_EP = "Při stahování alb interpreta zahrnout singly a EP ('0'-Ne,'1'-Ano):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Přidat ID před název složky s albem ('0'-Ne,'1'-Ano):"
    CHANGE_SAVE_COVERS = "Uložit obaly alb ('0'-Ne,'1'-Ano):"
    CHANGE_LANGUAGE = "Zvolit jazyk"
    CHANGE_ALBUM_FOLDER_FORMAT = "Formát názvu složky alba ('0' beze změny):"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Playlist folder format('0'-not modify,'default'-to set default):"
    CHANGE_TRACK_FILE_FORMAT = "Formát názvu složky skladny ('0' beze změny):"
    CHANGE_VIDEO_FILE_FORMAT = "Formát názvu souboru videa ('0'-beze změny,'default'-pro nastavení výchozího názvu):"
    CHANGE_SHOW_PROGRESS = "Zobrazit indikátor stavu stahování ('0'-Ne,'1'-Ano):"
    CHANGE_SHOW_TRACKINFO = "Zobrazit info o skladbě ('0'-Ne,'1'-Ano):"
    CHANGE_SAVE_ALBUM_INFO = "Uložit soubor AlbumInfo.txt ('0'-Ne,'1'-Ano):"
    CHANGE_DOWNLOAD_VIDEOS = "Download videos (when downloading playlists, albums, mixes)('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Přidat texty skladeb ('0'-Ne,'1'-Ano):"
    CHANGE_LYRICS_SERVER_PROXY = "Server proxy pro texty skladeb ('0' beze změny):"
    CHANGE_ADD_LRC_FILE = "Uložit slova skladby s časováním do souboru .lrc) ('0'-Ne,'1'-Ano):"
    CHANGE_ADD_TYPE_FOLDER = "Ukládat do složek dle typu obsahu, např. Album/Video/Playlist ('0'-Ne,'1'-Ano):"
    CHANGE_MULITHREAD_DOWNLOAD = "Více vláken pro stahování ('0'-Ne,'1'-Ano):"
    CHANGE_USE_DOWNLOAD_DELAY = "Stahovat s časovou prodlevou('0'-Ne,'1'-Ano):"
    CHANGE_ENABLE_LISTENER = "Enable listener mode('0'-No,'1'-Yes):"
    CHANGE_LISTENER_SECRET = "Listener secret('0'-not modify):"
    CHANGE_LISTENER_PORT = "Listener port('0'-not modify):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Spouštění přihlašovacího procesu..."
    AUTH_LOGIN_CODE = "Váš přihlašovací kód je {}"
    AUTH_NEXT_STEP = "K dokončení nastavení přejděte na stránku {} během následujích {}."
    AUTH_WAITING = "Čeká se na autorizaci..."
    AUTH_TIMEOUT = "Vypršel časový limit procesu."

    MSG_VALID_ACCESSTOKEN = "Přístupový token fukční pro {}."
    MSG_INVALID_ACCESSTOKEN = "Platnost přístupového tokenu vypršela. Pokouším se o obnovení."
    MSG_PATH_ERR = "Cesta neexistuje!"
    MSG_INPUT_ERR = "Chyba zadání!"

    MODEL_ALBUM_PROPERTY = "ALBUM-VLASTNOSTI"
    MODEL_TRACK_PROPERTY = "SKLADBA-VLASTNOSTI"
    MODEL_VIDEO_PROPERTY = "VIDEO-VLASTNOSTI"
    MODEL_ARTIST_PROPERTY = "INTERPRET-VLASTNOSTI"
    MODEL_PLAYLIST_PROPERTY = "PLAYLIST-VLASTNOSTI"

    MODEL_TITLE = 'Název skladby'
    MODEL_TRACK_NUMBER = 'Číslo skladby'
    MODEL_VIDEO_NUMBER = 'Číslo videa'
    MODEL_RELEASE_DATE = 'Datum vydání'
    MODEL_VERSION = 'Verze'
    MODEL_EXPLICIT = 'Explicitní'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Jméno'
    MODEL_TYPE = 'Typ'
