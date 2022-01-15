#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   arabic.py
@Time    :   2020/08/19
@Author  :   shhade for hack
@Version :   1.0
@Contact :   
@Desc    :   
'''


class LangArabic(object):
    SETTING = "الاعدادت"
    VALUE = "القيمة"
    SETTING_DOWNLOAD_PATH = "مجلد التحميل"
    SETTING_ONLY_M4A = "تحويل m4a الى mp4"
    SETTING_ADD_EXPLICIT_TAG = "اضافة توقيع الفنان"
    SETTING_ADD_HYPHEN = "اضافة سطر تحتي"
    SETTING_ADD_YEAR = "اضافة سنة الاصدار قبل نجلد التنزيل"
    SETTING_USE_TRACK_NUM = "اضف رقم التتبع الخاص بالاغنية"
    SETTING_AUDIO_QUALITY = "دقة الصوت"
    SETTING_VIDEO_QUALITY = "دقة الفديو"
    SETTING_CHECK_EXIST = "التاكد من وجود الملف قبل التنزيل"
    SETTING_CHECK_ALBUM_EXIST = "تحقق من وجود الألبوم"
    SETTING_ARTIST_BEFORE_TITLE = "اسم الفنان قبل اسم الاغنية"
    SETTING_ALBUMID_BEFORE_FOLDER = "رقم التتبع قبل مجلد التنزيل"
    SETTING_INCLUDE_EP = "اضافة single&ep"
    SETTING_SAVE_COVERS = "حفظ صورة الالبوم"
    SETTING_LANGUAGE = "اللغة"
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

    CHOICE = "خيار"
    FUNCTION = "وظيفة"
    CHOICE_ENTER = "ادخل"
    CHOICE_ENTER_URLID = "ادخل 'رابط/رقم تتبع':"
    CHOICE_EXIT = "اخرج"
    CHOICE_LOGIN = "Check AccessToken"
    CHOICE_SETTINGS = "الاعدادات"
    CHOICE_SET_ACCESS_TOKEN = "اعداد AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "التحميل عبر الرابط او رقم التتبع"
    CHOICE_LOGOUT = "Logout"
    CHOICE_APIKEY = "Select APIKey"

    PRINT_ERR = "[خطأ]"
    PRINT_INFO = "[معلومة]"
    PRINT_SUCCESS = "[نجاح]"

    PRINT_ENTER_CHOICE = "ادخل الخيار:"
    PRINT_LATEST_VERSION = "آخر اصدر:"
    # PRINT_USERNAME = "اسم المستخدم:"
    # PRINT_PASSWORD = "رمز الدخول:"

    CHANGE_START_SETTINGS = "بدء الاعدادات('0'-Return,'1'-Yes):"
    CHANGE_DOWNLOAD_PATH = "مجلد التنزيل('0' not modify):"
    CHANGE_AUDIO_QUALITY = "دقة الصوت('0'-Normal,'1'-High,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "دقة الفديو(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "تحويل M4a الى mp4('0'-No,'1'-Yes):"
    CHANGE_ADD_EXPLICIT_TAG = "اضافة توقيع الفنان('0'-No,'1'-Yes):"
    CHANGE_ADD_HYPHEN = "استخدم السطور التحتية بدل الفراغات('0'-No,'1'-Yes):"
    CHANGE_ADD_YEAR = "اضافة سنة الاصدار الى مجلد الالبوم('0'-No,'1'-Yes):"
    CHANGE_USE_TRACK_NUM = "اضافة رقم الاغنية قبل اسمها('0'-No,'1'-Yes):"
    CHANGE_CHECK_EXIST = "التحقق من وجود الملف قبل التحميل('0'-No,'1'-Yes):"
    CHANGE_CHECK_ALBUM_EXIST = "تحقق مما إذا كان الألبوم موجودًا قبل التنزيل('0'-No,'1'-Yes):"
    CHANGE_ARTIST_BEFORE_TITLE = "اضف اسم الفنان قبل اسم الاغنية('0'-No,'1'-Yes):"
    CHANGE_INCLUDE_EP = "اضافة مسطلحات فردي او ثنائي الى الغنية('0'-No,'1'-Yes):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "اضف رقم التتبع قبل اسم مجلد الالبوم('0'-No,'1'-Yes):"
    CHANGE_SAVE_COVERS = "حفظ صورة الالبوم('0'-No,'1'-Yes):"
    CHANGE_LANGUAGE = "اختر لغة"
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
    MSG_PATH_ERR = "!مجلد التنزيل خاطئ"
    MSG_INPUT_ERR = "!ادخال خاطئ"

    MODEL_ALBUM_PROPERTY = "ملكية الالبوم"
    MODEL_TRACK_PROPERTY = "ملكية الاغنية"
    MODEL_VIDEO_PROPERTY = "ملكية الفديو"
    MODEL_ARTIST_PROPERTY = "ملكية الفنان"
    MODEL_PLAYLIST_PROPERTY = "ملكية قائمة الاغاني"

    MODEL_TITLE = 'الاسم'
    MODEL_TRACK_NUMBER = 'رقم الاغنية'
    MODEL_VIDEO_NUMBER = 'رقم الفديو'
    MODEL_RELEASE_DATE = 'عام الاصدار'
    MODEL_VERSION = 'الاصدار'
    MODEL_EXPLICIT = 'توقيع الفنان'
    MODEL_ALBUM = 'الالبوم'
    MODEL_ID = 'رقم التتبع'
    MODEL_NAME = 'الاسم'
    MODEL_TYPE = 'النوع'
