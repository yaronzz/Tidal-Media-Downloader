#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   polish.py
@Time    :   2022/03/04
@Author  :   PatrykMis
@Version :   1.0
@Contact :   patryk.mis@member.fsf.org
@Desc    :   
'''


class LangPolish(object):
    SETTING = "USTAWIENIA"
    VALUE = "WARTOŚĆ"
    SETTING_DOWNLOAD_PATH = "Ścieżka pobierania"
    SETTING_ONLY_M4A = "Konwertuj mp4 do m4a"
    SETTING_ADD_EXPLICIT_TAG = "Dodaj tag jednoznaczne"
    SETTING_ADD_HYPHEN = "Dodaj myslnik"
    SETTING_ADD_YEAR = "Dodaj rok porzed folderem albumu"
    SETTING_USE_TRACK_NUM = "Dodaj numer utworu użytkownika"
    SETTING_AUDIO_QUALITY = "Jakość audio"
    SETTING_VIDEO_QUALITY = "Jakość wideo"
    SETTING_CHECK_EXIST = "Sprawdź istnienie"
    SETTING_ARTIST_BEFORE_TITLE = "Nazwa artysty przed tytułem utworu"
    SETTING_ALBUMID_BEFORE_FOLDER = "Id przed folderem albumu"
    SETTING_INCLUDE_EP = "Uwzględnij single i EP"
    SETTING_SAVE_COVERS = "Zapisz okładki"
    SETTING_LANGUAGE = "Język"
    SETTING_USE_PLAYLIST_FOLDER = "Użyj folder playlisty"
    SETTING_MULITHREAD_DOWNLOAD = "Pobieranie wielowątkowe"
    SETTING_ALBUM_FOLDER_FORMAT = "Format folderu albumu"
    SETTING_PLAYLIST_FOLDER_FORMAT = "Playlist folder format"
    SETTING_TRACK_FILE_FORMAT = "Format pliku utworu"
    SETTING_VIDEO_FILE_FORMAT = "Video file format"
    SETTING_SHOW_PROGRESS = "Pokaż postęp"
    SETTING_SHOW_TRACKINFO = "Pokaż informacje o utworze"
    SETTING_SAVE_ALBUMINFO = "Zapisz AlbumInfo.txt"
    SETTING_DOWNLOAD_VIDEOS = "Download videos"
    SETTING_ADD_LYRICS = "Dodaj teksty utworów"
    SETTING_LYRICS_SERVER_PROXY = "Serwer proxy dla tekstów"
    SETTING_ADD_LRC_FILE = "Zapisz czasowe teksty utworów (plik .lrc)"
    SETTING_PATH = "Ścieżka ustawień"
    SETTING_APIKEY = "Obsługa APIKey"
    SETTING_ADD_TYPE_FOLDER = "Dodaj folder typu"
    SETTING_DOWNLOAD_DELAY = "Use Download Delay"
    SETTING_LISTENER_ENABLED = "Listener mode enabled"
    SETTING_LISTENER_PORT = "Listener port"
    SETTING_LISTENER_SECRET = "Listener secret"

    CHOICE = "WYBÓR"
    FUNCTION = "FUNKCJA"
    CHOICE_ENTER = "Wpisz"
    CHOICE_ENTER_URLID = "Wpisz 'Url/ID':"
    CHOICE_EXIT = "Wyjdź"
    CHOICE_LOGIN = "Sprawdź AccessToken"
    CHOICE_SETTINGS = "Ustawienia"
    CHOICE_SET_ACCESS_TOKEN = "Ustaw AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Pobierz według adresu URL lub ID"
    CHOICE_LOGOUT = "Wyloguj"
    CHOICE_APIKEY = "Wybierz APIKey"
    CHOICE_PKCE_LOGIN = "Login via PKCE"
    CHOICE_LISTENER = "Start listener mode"

    PRINT_ERR = "[BŁĄD]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[SUKCES]"

    PRINT_ENTER_CHOICE = "Wprowadź Wybór:"
    PRINT_LATEST_VERSION = "Najnowsza wersja:"
    # PRINT_USERNAME = "nazwa użytkownika:"
    # PRINT_PASSWORD = "hasło:"

    CHANGE_START_SETTINGS = "Uruchomić ustawienia('0'-Powrót,'1'-Tak):"
    CHANGE_DOWNLOAD_PATH = "Ścieżka pobierania('0'-bez zmian):"
    CHANGE_AUDIO_QUALITY = "Jakość audio('0'-Normalna,'1'-Wysoka,'2'-HiFi,'3'-Master,'4'-Max):"
    CHANGE_VIDEO_QUALITY = "Jakość wideo(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Konwertuj mp4 do m4a('0'-Nie,'1'-Tak):"
    CHANGE_ADD_EXPLICIT_TAG = "Dodaj tag jednoznaczne do nazwy pliku('0'-Nie,'1'-Tak):"
    CHANGE_ADD_HYPHEN = "Używaj myślników zamiast spacji w nazwach plików('0'-Nie,'1'-Tak):"
    CHANGE_ADD_YEAR = "Dodaj rok do nazw folderów albumów('0'-Nie,'1'-Tak):"
    CHANGE_USE_TRACK_NUM = "Dodaj numer utworu przed nazwami plików('0'-Nie,'1'-Tak):"
    CHANGE_CHECK_EXIST = "Sprawdź istniejący plik przed pobraniem utworu('0'-Nie,'1'-Tak):"
    CHANGE_ARTIST_BEFORE_TITLE = "Dodaj nazwę artysty przed tytułem utworu('0'-Nie,'1'-Tak):"
    CHANGE_INCLUDE_EP = "Uwzględnij single i EP podczas pobierania albumów wykonawcy('0'-Nie,'1'-Tak):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Dodaj ID przed folderem albumu('0'-Nie,'1'-Tak):"
    CHANGE_SAVE_COVERS = "Zapisz okładki('0'-Nie,'1'-Tak):"
    CHANGE_LANGUAGE = "Wybierz język"
    CHANGE_ALBUM_FOLDER_FORMAT = "Format folderu albumu('0'-nie modyfikuj,'default'-by ustawić domyślny):"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Playlist folder format('0'-not modify,'default'-to set default):"
    CHANGE_TRACK_FILE_FORMAT = "Format pliku utworu('0'-nie modyfikuj,'default'-by ustawić domyślny):"
    CHANGE_VIDEO_FILE_FORMAT = "Video file format('0'-not modify,'default'-to set default):"
    CHANGE_SHOW_PROGRESS = "Pokaż postęp('0'-Nie,'1'-Tak):"
    CHANGE_SHOW_TRACKINFO = "Pokaż informacje o utworze('0'-Nie,'1'-Tak):"
    CHANGE_SAVE_ALBUM_INFO = "Zapisz AlbumInfo.txt('0'-Nie,'1'-Tak):"
    CHANGE_DOWNLOAD_VIDEOS = "Download videos (when downloading playlists, albums, mixes)('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Dodaj teksty utworów('0'-Nie,'1'-Tak):"
    CHANGE_LYRICS_SERVER_PROXY = "Serwer proxy dla tekstów('0'-nie modyfikuj):"
    CHANGE_ADD_LRC_FILE = "Zapisz plik .lrc czasowych tekstów utworów ('0'-Nie,'1'-Tak):"
    CHANGE_ADD_TYPE_FOLDER = "Dodaj folder typu, np. Album/wideo/lista odtwarzania('0'-Nie,'1'-Tak):"
    CHANGE_MULITHREAD_DOWNLOAD = "Multi thread download('0'-No,'1'-Yes):"
    CHANGE_USE_DOWNLOAD_DELAY = "Use Download Delay('0'-No,'1'-Yes):"
    CHANGE_ENABLE_LISTENER = "Enable listener mode('0'-No,'1'-Yes):"
    CHANGE_LISTENER_SECRET = "Listener secret('0'-not modify):"
    CHANGE_LISTENER_PORT = "Listener port('0'-not modify):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Rozpoczęcie procesu logowania..."
    AUTH_LOGIN_CODE = "Twój kod logowania to {}"
    AUTH_NEXT_STEP = "Przejdź do {} w ciągu następnych {} aby zakończyć konfigurację."
    AUTH_WAITING = "Oczekiwanie na autoryzację..."
    AUTH_TIMEOUT = "Przekroczono limit czasu operacji."

    MSG_VALID_ACCESSTOKEN = "AccessToken dobry przez {}."
    MSG_INVALID_ACCESSTOKEN = "AccessToken wygasł. Próba jego odświeżenia."
    MSG_PATH_ERR = "Ścieżka jest błędna!"
    MSG_INPUT_ERR = "Błąd wejścia!"

    MODEL_ALBUM_PROPERTY = "ALBUM-WŁAŚCIWOŚĆ"
    MODEL_TRACK_PROPERTY = "UTWÓR-WŁAŚCIWOŚĆ"
    MODEL_VIDEO_PROPERTY = "WIDEO-WŁAŚCIWOŚĆ"
    MODEL_ARTIST_PROPERTY = "ARTYSTA-WŁAŚCIWOŚĆ"
    MODEL_PLAYLIST_PROPERTY = "PLAYLISTA-WŁAŚCIWOŚĆ"

    MODEL_TITLE = 'Tytuł'
    MODEL_TRACK_NUMBER = 'Numer Utworu'
    MODEL_VIDEO_NUMBER = 'Numer Wideo'
    MODEL_RELEASE_DATE = 'Data Wydania'
    MODEL_VERSION = 'Wersja'
    MODEL_EXPLICIT = 'Jednoznaczny'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Nazwa'
    MODEL_TYPE = 'Typ'
