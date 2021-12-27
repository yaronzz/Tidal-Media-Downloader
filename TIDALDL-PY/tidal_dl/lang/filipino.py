#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   filipino.py
@Time    :   2020/08/21
@Author  :   Ni Ño
@Version :   1.0
@Contact :   
@Desc    :   
'''


class LangFilipino(object):
    SETTING = "SETTINGS"
    VALUE = "VALUE"
    SETTING_DOWNLOAD_PATH = "Paroroonan ng Download"
    SETTING_ONLY_M4A = "I-convert ang mp4 bilang m4a"
    SETTING_ADD_EXPLICIT_TAG = "Lagyan ng explicit tag"
    SETTING_ADD_HYPHEN = "Lagyan ng hyphen"
    SETTING_ADD_YEAR = "Lagyan ng taon bago ang album-folder"
    SETTING_USE_TRACK_NUM = "Lagyan ng bilang ng user track"
    SETTING_AUDIO_QUALITY = "Kalidad ng Audio"
    SETTING_VIDEO_QUALITY = "Kalidad ng Video"
    SETTING_CHECK_EXIST = "Suriin kung mayroon na"
    SETTING_ARTIST_BEFORE_TITLE = "Pangalan ng artist bago ang pamagat ng kanta"
    SETTING_ALBUMID_BEFORE_FOLDER = "Id bago ang album-folder"
    SETTING_INCLUDE_EP = "Isama ang single at ep"
    SETTING_SAVE_COVERS = "I-save ang mga cover"
    SETTING_LANGUAGE = "Lenggwahe"
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

    CHOICE = "PAGPIPILIAN"
    FUNCTION = "SILBI"
    CHOICE_ENTER = "Ilagay"
    CHOICE_ENTER_URLID = "Ilagay ang 'Url/ID':"
    CHOICE_EXIT = "Mag Exit"
    CHOICE_LOGIN = "Check AccessToken"
    CHOICE_SETTINGS = "Settings"
    CHOICE_SET_ACCESS_TOKEN = "I-set ang AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Mag download gamit ang url o id"
    CHOICE_LOGOUT = "Logout"
    CHOICE_APIKEY = "Select APIKey"

    PRINT_ERR = "[ERR]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[TAPOS NA]"

    PRINT_ENTER_CHOICE = "Pumili ng sagot:"
    PRINT_LATEST_VERSION = "Pinakabagong Version:"
    # PRINT_USERNAME = "username:"
    # PRINT_PASSWORD = "password:"

    CHANGE_START_SETTINGS = "Simulan ang settings('0'-Bumalik,'1'-Oo):"
    CHANGE_DOWNLOAD_PATH = "Paroroonan ng Download('0' walang babaguhin):"
    CHANGE_AUDIO_QUALITY = "Kalidad ng Audio('0'-Normal,'1'-High,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Kalidad ng Audio Video(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "I-convert ang mp4 bilang m4a('0'-Hindi,'1'-Oo):"
    CHANGE_ADD_EXPLICIT_TAG = "Lagyan ng explicit tag sa pangalan ng files('0'-Hindi,'1'-Oo):"
    CHANGE_ADD_HYPHEN = "Gamitin ang hyphens kesa sa spaces sa pangalan ng files('0'-Hindi,'1'-Oo):"
    CHANGE_ADD_YEAR = "Lagyan ng taon sa pangalan ng album folder('0'-Hindi,'1'-Oo):"
    CHANGE_USE_TRACK_NUM = "Lagyan ng bilang ng track bago ang pangalan ng files('0'-Hindi,'1'-Oo):"
    CHANGE_CHECK_EXIST = "Suriin kung naidownload na bago mag download muli('0'-Hindi,'1'-Oo):"
    CHANGE_ARTIST_BEFORE_TITLE = "Lagyan ng pangalan ng artist bago ang pamagat ng kanta('0'-Hindi,'1'-Oo):"
    CHANGE_INCLUDE_EP = "Isama ang singles at EPs sa pagdownload ng mga album mula sa artist('0'-Hindi,'1'-Oo):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Lagyan ng id bago ang album folder('0'-Hindi,'1'-Oo):"
    CHANGE_SAVE_COVERS = "I-save ang mga covers('0'-Hindi,'1'-Oo):"
    CHANGE_LANGUAGE = "Pumili ng lenggwahe"
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
    MSG_PATH_ERR = "May error sa paroroonan ng download!"
    MSG_INPUT_ERR = "May error sa pag-input!"

    MODEL_ALBUM_PROPERTY = "PROPERTY NG ALBUM"
    MODEL_TRACK_PROPERTY = "PROPERTY NG TRACK"
    MODEL_VIDEO_PROPERTY = "PROPERTY NG VIDEO"
    MODEL_ARTIST_PROPERTY = "PROPERTY NG ARTIST"
    MODEL_PLAYLIST_PROPERTY = "PROPERTY NG PLAYLIST"

    MODEL_TITLE = 'Pamagat'
    MODEL_TRACK_NUMBER = 'Bilang ng Track'
    MODEL_VIDEO_NUMBER = 'Bilang ng Video'
    MODEL_RELEASE_DATE = 'Petsa ng Pag-release'
    MODEL_VERSION = 'Bersyon'
    MODEL_EXPLICIT = 'Explicit'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Pangalan'
    MODEL_TYPE = 'Uri'
