#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   russian.py
@Time    :   2025/01/09
@Author  :   sergey.seve-s, Pal
@Version :   1.1
@Contact :   
@Desc    :   Обновлены непереведённые строки
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
    SETTING_USE_PLAYLIST_FOLDER = "Плейлисты в отдельную папку"
    SETTING_MULITHREAD_DOWNLOAD = "Многопоточная загрузка"
    SETTING_ALBUM_FOLDER_FORMAT = "Маска имени альбома"
    SETTING_PLAYLIST_FOLDER_FORMAT = "Формат папок плейлиста"
    SETTING_TRACK_FILE_FORMAT = "Маска имени трека"
    SETTING_VIDEO_FILE_FORMAT = "Формат видеофайла"
    SETTING_SHOW_PROGRESS = "Показывать процесс загрузки"
    SETTING_SHOW_TRACKINFO = "Показывать информацию о треке"
    SETTING_SAVE_ALBUMINFO = "Сохранять AlbumInfo.txt"
    SETTING_DOWNLOAD_VIDEOS = "Скачивать видео"
    SETTING_ADD_LYRICS = "Добавлять текст песень"
    SETTING_LYRICS_SERVER_PROXY = "Прокси сервер для текстов песен"
    SETTING_ADD_LRC_FILE = "Сохранять синхронизированный текст в .lrc файл"
    SETTING_PATH = "Путь для настроек"
    SETTING_APIKEY = "Поддержка APIKey"
    SETTING_ADD_TYPE_FOLDER = "Добавить подпапки"
    SETTING_DOWNLOAD_DELAY = "Использовать задержку загрузки"

    CHOICE = "ВЫБРАТЬ"
    FUNCTION = "ФУНКЦИИ"
    CHOICE_ENTER = "Ввод"
    CHOICE_ENTER_URLID = "Ввод 'Url/ID':"
    CHOICE_EXIT = "Выход"
    CHOICE_LOGIN = "Проверить AccessToken"
    CHOICE_SETTINGS = "Настройки"
    CHOICE_SET_ACCESS_TOKEN = "Применить AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Использовать ссылку для загрузки"
    CHOICE_LOGOUT = "Переподключение"
    CHOICE_APIKEY = "Выбрать APIKey"

    PRINT_ERR = "[ОШИБКА]"
    PRINT_INFO = "[СВЕДЕНИЯ]"
    PRINT_SUCCESS = "[ГОТОВО]"

    PRINT_ENTER_CHOICE = "Выбор функции:"
    PRINT_LATEST_VERSION = "Последняя версия:"
    # PRINT_USERNAME = "Имя:"
    # PRINT_PASSWORD = "Пароль:"

    CHANGE_START_SETTINGS = "Начальная настройка('0'-Отмена,'1'-Да):"
    CHANGE_DOWNLOAD_PATH = "Место сохранения('0'-Отмена):"
    CHANGE_AUDIO_QUALITY = "Качество аудио('0'-Стандарт,'1'-Высокое,'2'-HiFi,'3'-MQA,'4'-Max):"
    CHANGE_VIDEO_QUALITY = "Качество видео(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Сохранять mp4 как m4a('0'-Нет,'1'-Да):"
    CHANGE_ADD_EXPLICIT_TAG = "Добавить тег 'Нецензурно(18+)' ('0'-Нет,'1'-Да):"
    CHANGE_ADD_HYPHEN = "Использовать дефис вместо пробела в имени файла трека('0'-Нет,'1'-Да):"
    CHANGE_ADD_YEAR = "Добавлять год выхода перед названием альбома('0'-Нет,'1'-Да):"
    CHANGE_USE_TRACK_NUM = "Добавить порядковый номер в альбоме перед названием трека('0'-Нет,'1'-Да):"
    CHANGE_CHECK_EXIST = "Проверять наличие перед загрузкой('0'-Нет,'1'-Да):"
    CHANGE_ARTIST_BEFORE_TITLE = "Добавить имя артиста перед названием трека('0'-Нет,'1'-Да):"
    CHANGE_INCLUDE_EP = "Включать синглы и миньоны в дискографию('0'-Нет,'1'-Да):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Добавить ID перед названием альбома('0'-Нет,'1'-Да):"
    CHANGE_SAVE_COVERS = "Сохранять обложки('0'-Нет,'1'-Да):"
    CHANGE_LANGUAGE = "Выбрать язык"
    CHANGE_ALBUM_FOLDER_FORMAT = "Маска имени альбома('0'-не менять):"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Формат папок плейлиста('0'-не менять,'default'-установить стандартный формат):"
    CHANGE_TRACK_FILE_FORMAT = "Маска имени трека('0'-не менять):"
    CHANGE_VIDEO_FILE_FORMAT = "Формат видеофайла('0'-не менять,'default'-установить стандартный формат):"
    CHANGE_SHOW_PROGRESS = "Показывать процесс загрузки('0'-Нет,'1'-Да):"
    CHANGE_SHOW_TRACKINFO = "Показывать информацию о треке('0'-Нет,'1'-Да):"
    CHANGE_SAVE_ALBUM_INFO = "Сохранять AlbumInfo.txt('0'-Нет,'1'-Да):"
    CHANGE_DOWNLOAD_VIDEOS = "Скачивать видео (когда скачиваются плейлисты, альбомы, миксы) ('0'-Нет,'1'-Да):"
    CHANGE_ADD_LYRICS = "Добавлять тексты песен('0'-Нет,'1'-Да):"
    CHANGE_LYRICS_SERVER_PROXY = "Прокси для сервера с текстом песен('0'-не менять):"
    CHANGE_ADD_LRC_FILE = "Сохранять синхронизированный текст в .lrc файл('0'-Нет,'1'-Да):"
    CHANGE_ADD_TYPE_FOLDER = "Добавить подпапки типов, те Альбом/Видео/Плейлист('0'-Нет,'1'-Да):"
    CHANGE_MULITHREAD_DOWNLOAD = "Мультипоточное скачивание('0'-Нет,'1'-Да):"
    CHANGE_USE_DOWNLOAD_DELAY = "Использовать задержку загрузки('0'-Нет,'1'-Да):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Входим в сервис..."
    AUTH_LOGIN_CODE = "Ваш код для входа {}"
    AUTH_NEXT_STEP = "Перейдите к {} в течении {}, для завершения настройки."
    AUTH_WAITING = "Ожидание авторизации..."
    AUTH_TIMEOUT = "Закончилось время ожидания."

    MSG_VALID_ACCESSTOKEN = "AccessToken успешно применён {}."
    MSG_INVALID_ACCESSTOKEN = "Срок действия AccessToken истек.  Попытка обновления."
    MSG_PATH_ERR = "Неверное место!"
    MSG_INPUT_ERR = "Ошибка ввода!"

    MODEL_ALBUM_PROPERTY = "СВОЙСТВА-АЛЬБОМА"
    MODEL_TRACK_PROPERTY = "СВОЙСТВА-ТРЕКА"
    MODEL_VIDEO_PROPERTY = "СВОЙСТВА-ВИДЕО"
    MODEL_ARTIST_PROPERTY = "СВОЙСТВА-АВТОРА"
    MODEL_PLAYLIST_PROPERTY = "СВОЙСТВА-ПЛЕЙЛИСТА"

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
