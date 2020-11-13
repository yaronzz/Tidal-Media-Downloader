#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   russian.py
@Time    :   2020/08/19
@Author  :   sergey.seve-s
@Version :   1.0
@Contact :   
@Desc    :   
'''

class LangRussian(object):
    SETTING = "НАСТРОЙКА"
    VALUE = "УСТАНОВКА"
    SETTING_DOWNLOAD_PATH = "Место сохранения"
    SETTING_ONLY_M4A = "Сохранять mp4 как m4a"
    SETTING_ADD_EXPLICIT_TAG = "Добавить тег Нецензурно"
    SETTING_ADD_HYPHEN = "Добавить дефис"
    SETTING_ADD_YEAR = "Добавить год перед именем папки-альбома"
    SETTING_USE_TRACK_NUM = "Добавить номер трека"
    SETTING_AUDIO_QUALITY = "Качество аудио"
    SETTING_VIDEO_QUALITY = "Качество видео"
    SETTING_CHECK_EXIST = "Проверять наличие"
    SETTING_ARTIST_BEFORE_TITLE = "Исполнитель перед названием трека"
    SETTING_ALBUMID_BEFORE_FOLDER = "ID перед названием папки"
    SETTING_INCLUDE_EP = "Включить сингл и миньон"
    SETTING_SAVE_COVERS = "Добавлять обложку"
    SETTING_LANGUAGE = "Язык"
    SETTING_USE_PLAYLIST_FOLDER = "Use playlist folder"
    SETTING_MULITHREAD_DOWNLOAD = "Multi thread download"
    SETTING_ALBUM_FOLDER_FORMAT = "Album folder format"
    SETTING_TRACK_FILE_FORMAT = "Track file format"
    SETTING_SHOW_PROGRESS = "Show progress"

    CHOICE = "ВЫБРАТЬ"
    FUNCTION = "ФУНКЦИИ"
    CHOICE_ENTER = "Ввод"
    CHOICE_ENTER_URLID = "Ввод 'Url/ID':"
    CHOICE_EXIT = "Выход"
    CHOICE_LOGIN = "Check AccessToken"
    CHOICE_SETTINGS = "Настройки"
    #CHOICE_SET_ACCESS_TOKEN = "Применить AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Использовать ссылку для загрузки"
    CHOICE_LOGOUT = "Logout"

    PRINT_ERR = "[ОШИБКА]"
    PRINT_INFO = "[СВЕДЕНИЯ]"
    PRINT_SUCCESS = "[ГОТОВО]"

    PRINT_ENTER_CHOICE = "Выбор функции:"
    PRINT_LATEST_VERSION = "Последняя версия:"
    #PRINT_USERNAME = "Имя:"
    #PRINT_PASSWORD = "Пароль:"
    
    CHANGE_START_SETTINGS = "Начальная настройка('0'-Отмена,'1'-Да):"
    CHANGE_DOWNLOAD_PATH = "Место сохранения('0'-Отмена):"
    CHANGE_AUDIO_QUALITY = "Качество аудио('0'-Стандарт,'1'-Высокое,'2'-HiFi,'3'-MQA):"
    CHANGE_VIDEO_QUALITY = "Качество видео('0'-1080,'1'-720,'2'-480,'3'-360):"
    CHANGE_ONLYM4A = "Сохранять mp4 как m4a('0'-Нет,'1'-Да):"
    CHANGE_ADD_EXPLICIT_TAG = "Добавить тег 'Нецензурно' ('0'-Нет,'1'-Да):"
    CHANGE_ADD_HYPHEN = "Использовать дефис вместо пробела в имени трека('0'-Нет,'1'-Да):"
    CHANGE_ADD_YEAR = "Добавлять год перед названием альбома('0'-Нет,'1'-Да):"
    CHANGE_USE_TRACK_NUM = "Добавить номер перед названием трека('0'-Нет,'1'-Да):"
    CHANGE_CHECK_EXIST = "Проверять наличие перед загрузкой('0'-Нет,'1'-Да):"
    CHANGE_ARTIST_BEFORE_TITLE = "Добавить имя артиста перед названием трека('0'-Нет,'1'-Да):"
    CHANGE_INCLUDE_EP = "Включать синглы и миньоны в дискографию('0'-Нет'1'-Да):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Добавить ID перед названием альбома('0'-Нет,'1'-Да):"
    CHANGE_SAVE_COVERS = "Сохранять обложки('0'-Нет,'1'-Да):"
    CHANGE_LANGUAGE = "Выбрать язык"
    CHANGE_ALBUM_FOLDER_FORMAT = "Album folder format('0' not modify):"
    CHANGE_TRACK_FILE_FORMAT = "Track file format('0' not modify):"
    CHANGE_SHOW_PROGRESS = "Show progress('0'-No,'1'-Yes):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Starting login process..."
    AUTH_LOGIN_CODE = "Your login code is {}"
    AUTH_NEXT_STEP = "Go to {} within the next {} to complete setup."
    AUTH_WAITING = "Waiting for authorization..."
    AUTH_TIMEOUT = "Operation timed out."
    
    MSG_VALID_ACCESSTOKEN = "AccessToken good for {}."
    MSG_INVAILD_ACCESSTOKEN = "Expired AccessToken. Attempting to refresh it."
    MSG_PATH_ERR = "Неверное место!"
    MSG_INPUT_ERR = "Ошибка ввода!"

    MODEL_ALBUM_PROPERTY = "ALBUM-PROPERTY"
    MODEL_TRACK_PROPERTY = "TRACK-PROPERTY"
    MODEL_VIDEO_PROPERTY = "VIDEO-PROPERTY"
    MODEL_ARTIST_PROPERTY = "ARTIST-PROPERTY"
    MODEL_PLAYLIST_PROPERTY = "PLAYLIST-PROPERTY"

    MODEL_TITLE = 'Название'
    MODEL_TRACK_NUMBER = 'Номер трека'
    MODEL_VIDEO_NUMBER = 'Номер видео'
    MODEL_RELEASE_DATE = 'Дата издания'
    MODEL_VERSION = 'Версия'
    MODEL_EXPLICIT = 'Нецензурно'
    MODEL_ALBUM = 'Альбом'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Имя'
    MODEL_TYPE = 'Тип'
