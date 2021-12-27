#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ukrainian.py
@Time    :   2020/09/07
@Author  :   Montyzzz
@Version :   1.0
@Contact :   ---
@Desc    :   
'''


class LangUkrainian(object):
    SETTING = "НАЛАШТУВАННЯ"
    VALUE = "ЗНАЧЕННЯ"
    SETTING_DOWNLOAD_PATH = "Шлях завантаження"
    SETTING_ONLY_M4A = "Перетворити mp4 на m4a"
    SETTING_ADD_EXPLICIT_TAG = "Додати тег Нецензурно"
    SETTING_ADD_HYPHEN = "Додати дефіс"
    SETTING_ADD_YEAR = "Додати рік перед ім'ям папки-альбому"
    SETTING_USE_TRACK_NUM = "Додати номер треку"
    SETTING_AUDIO_QUALITY = "Якість аудіо"
    SETTING_VIDEO_QUALITY = "Якість відео"
    SETTING_CHECK_EXIST = "Перевіряти наявність"
    SETTING_ARTIST_BEFORE_TITLE = "Виконавець перед назвою треку"
    SETTING_ALBUMID_BEFORE_FOLDER = "ID перед назвою теки"
    SETTING_INCLUDE_EP = "Включити сингл і міньйон"
    SETTING_SAVE_COVERS = "Зберегти обкладинки"
    SETTING_LANGUAGE = "Мова"
    SETTING_USE_PLAYLIST_FOLDER = "Use playlist folder"
    SETTING_MULITHREAD_DOWNLOAD = "Multi thread download"
    SETTING_ALBUM_FOLDER_FORMAT = "Album folder format"
    SETTING_TRACK_FILE_FORMAT = "Track file format"
    SETTING_SHOW_PROGRESS = "Show progress"
    SETTING_SHOW_TRACKIFNO = "Show Track Info"
    SETTING_SAVE_ALBUMINFO = "Save AlbumInfo.txt"
    SETTING_ADD_LYRICS = "Add lyrics"
    SETTING_LYRICS_SERVER_PROXY = "Lyrics server proxy"
    SETTING_PATH = "Settings path"
    SETTINGS_ADD_LRC_FILE = "Save timed lyrics (.lrc file)"
    SETTING_APIKEY = "APIKey support"
    SETTING_ADD_TYPE_FOLDER = "Add Type-Folder"

    CHOICE = "ВИБІР"
    FUNCTION = "ФУНКЦІЇ"
    CHOICE_ENTER = "Ввід"
    CHOICE_ENTER_URLID = "Ввід 'Url/ID':"
    CHOICE_EXIT = "Вихід"
    CHOICE_LOGIN = "Check AccessToken"
    CHOICE_SETTINGS = "Налаштування"
    CHOICE_SET_ACCESS_TOKEN = "Застосувати AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Завантажити за URL-адресою або ідентифікатором"
    CHOICE_LOGOUT = "Logout"
    CHOICE_APIKEY = "Select APIKey"

    PRINT_ERR = "[ПОМИЛКА]"
    PRINT_INFO = "[ІНФОРМАЦІЯ]"
    PRINT_SUCCESS = "[УСПІХ]"

    PRINT_ENTER_CHOICE = "Вибір вводу:"
    PRINT_LATEST_VERSION = "Остання версія:"
    # PRINT_USERNAME = "ім'я користувача:"
    # PRINT_PASSWORD = "пароль:"

    CHANGE_START_SETTINGS = "Налаштування запуску('0'-повернення,'1'-так):"
    CHANGE_DOWNLOAD_PATH = "Шлях завантаження('0' не змінювати):"
    CHANGE_AUDIO_QUALITY = "Якість аудіо('0'-Звичайна,'1'-Висока,'2'-HiFi,'3'-MQA):"
    CHANGE_VIDEO_QUALITY = "Якість відео(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Перетворити mp4 на m4a('0'-Ні,'1'-Так):"
    CHANGE_ADD_EXPLICIT_TAG = "Додати тег 'Нецензурно' ('0'-Ні,'1'-Так):"
    CHANGE_ADD_HYPHEN = "Використати дефіс замість пробілів в іменах файлів('0'-Ні,'1'-Так):"
    CHANGE_ADD_YEAR = "Додавати рік до назв тек альбомів ('0'-Ні,'1'-Так):"
    CHANGE_USE_TRACK_NUM = "Додавати номер доріжки перед назвами файлів ('0'-Ні,'1'-Так):"
    CHANGE_CHECK_EXIST = "Перевіряти наявний файл перед завантаженням треку ('0'-Ні,'1'-Так):"
    CHANGE_ARTIST_BEFORE_TITLE = "Додати ім’я виконавця перед заголовком треку ('0'-Ні,'1'-Так):"
    CHANGE_INCLUDE_EP = "Включати сингли та міньйони під час завантаження альбомів виконавця ('0'-Ні,'1'-Так):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Додати ідентифікатор перед текою альбому ('0'-Ні,'1'-Так):"
    CHANGE_SAVE_COVERS = "Зберігати обкладинки ('0'-Ні,'1'-Так):"
    CHANGE_LANGUAGE = "Обрати мову"
    CHANGE_ALBUM_FOLDER_FORMAT = "Album folder format('0' not modify):"
    CHANGE_TRACK_FILE_FORMAT = "Track file format('0' not modify):"
    CHANGE_SHOW_PROGRESS = "Show progress('0'-No,'1'-Yes):"
    CHANGE_SHOW_TRACKINFO = "Show track info('0'-No,'1'-Yes):"
    CHANGE_SAVE_ALBUM_INFO = "Save AlbumInfo.txt('0'-No,'1'-Yes):"
    CHANGE_ADD_LYRICS = "Add lyrics('0'-No,'1'-Yes):"
    CHANGE_LYRICS_SERVER_PROXY = "Lyrics server proxy('0' not modify):"
    CHANGE_ADD_LRC_FILE = "Save timed lyrics .lrc file ('0'-No,'1'-Yes):"
    CHANGE_ADD_TYPE_FOLDER = "Add Type-Folder,eg Album/Video/Playlist('0'-No,'1'-Yes):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Starting login process..."
    AUTH_LOGIN_CODE = "Your login code is {}"
    AUTH_NEXT_STEP = "Go to {} within the next {} to complete setup."
    AUTH_WAITING = "Waiting for authorization..."
    AUTH_TIMEOUT = "Operation timed out."

    MSG_VALID_ACCESSTOKEN = "AccessToken good for {}."
    MSG_INVAILD_ACCESSTOKEN = "Expired AccessToken. Attempting to refresh it."
    MSG_PATH_ERR = "Невірний шлях!"
    MSG_INPUT_ERR = "Помилка введення!"

    MODEL_ALBUM_PROPERTY = "ALBUM-PROPERTY"
    MODEL_TRACK_PROPERTY = "TRACK-PROPERTY"
    MODEL_VIDEO_PROPERTY = "VIDEO-PROPERTY"
    MODEL_ARTIST_PROPERTY = "ARTIST-PROPERTY"
    MODEL_PLAYLIST_PROPERTY = "PLAYLIST-PROPERTY"

    MODEL_TITLE = 'Назва'
    MODEL_TRACK_NUMBER = 'Номер доріжки'
    MODEL_VIDEO_NUMBER = 'Номер відео'
    MODEL_RELEASE_DATE = 'Дата релізу'
    MODEL_VERSION = 'Версія'
    MODEL_EXPLICIT = 'Нецензурно'
    MODEL_ALBUM = 'Альбом'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Ім\'я'
    MODEL_TYPE = 'Тип'
