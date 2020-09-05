#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   turkish.py
@Time    :   2020/08/20
@Author  :   shhade for hack
@Version :   1.0
@Contact :   
@Desc    :   
'''

class LangTurkish(object):
    SETTING = "AYARLAR"
    VALUE = "DEĞER"
    SETTING_DOWNLOAD_PATH = "Inenler dosyası"
    SETTING_ONLY_M4A = "mp4'ü m4a ya çevirmek"
    SETTING_ADD_EXPLICIT_TAG = "Açık etiketini ekle"
    SETTING_ADD_HYPHEN = "tire ekle"
    SETTING_ADD_YEAR = "Albüm-dosyasından önce yılı ekle"
    SETTING_USE_TRACK_NUM = "Kullanıcı takip numarasını ekle"
    SETTING_AUDIO_QUALITY = "Ses Kalitesi"
    SETTING_VIDEO_QUALITY = "Video Kalitesi"
    SETTING_CHECK_EXIST = "dosyanın olup olnadığına bak"
    SETTING_ARTIST_BEFORE_TITLE = "artist ismi şarkı-isminden önce"
    SETTING_ALBUMID_BEFORE_FOLDER = "Takip numarsı indirme dosyasından önce"
    SETTING_INCLUDE_EP = "ekle single&ep"
    SETTING_SAVE_COVERS = "kapak resmini kaydet"
    SETTING_LANGUAGE = "Dil"

    CHOICE = "SEÇENEK"
    FUNCTION = "FONKSİYON"
    CHOICE_ENTER = "Gir"
    CHOICE_ENTER_URLID = "Url/ID Gir:"
    CHOICE_EXIT = "Çık"
    CHOICE_LOGIN = "Giriş yap"
    CHOICE_SETTINGS = "Ayarlar"
    CHOICE_SET_ACCESS_TOKEN = "access token gir"
    CHOICE_DOWNLOAD_BY_URL = "id numarası veya web bağlantısıyla indir"

    PRINT_ERR = "[HATA]"
    PRINT_INFO = "[BILGI]"
    PRINT_SUCCESS = "[BAŞARILI]"

    PRINT_ENTER_CHOICE = "Seçeneği Gir:"
    PRINT_LATEST_VERSION = "Son Sürüm:"
    PRINT_USERNAME = "kullanıcı adı:"
    PRINT_PASSWORD = "şifre:"
    
    CHANGE_START_SETTINGS = "ayarları başlat('0'-dön,'1'-evet):"
    CHANGE_DOWNLOAD_PATH = "indirlenler dosyası('0' değişmesin):"
    CHANGE_AUDIO_QUALITY = "ses kalitesi('0'-Normal,'1'-Yüksek,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Video kalitesi('0'-1080,'1'-720,'2'-480,'3'-360):"
    CHANGE_ONLYM4A = "mp4 ü m4a ya çevir('0'-hayır,'1'-Evet):"
    CHANGE_ADD_EXPLICIT_TAG = "Açık etiketi ekle('0'-Hayır,'1'-Evet):"
    CHANGE_ADD_HYPHEN = "boşluk yerine satır ekle('0'-Hayır,'1'-Evet):"
    CHANGE_ADD_YEAR = "Albüm dosyasına albümün çıkış yılını ekle('0'-Hayır,'1'-Evet):"
    CHANGE_USE_TRACK_NUM = "şarkı numarasını şarkı isminden önce ekle('0'-Hayır,'1'-Evet):"
    CHANGE_CHECK_EXIST = "indirmeden önce dosyanın olup olmadığın kontrol et('0'-Hayır,'1'-Evet):"
    CHANGE_ARTIST_BEFORE_TITLE = "artist adını şarkı isminden önce ekle('0'-Hayır,'1'-Evet):"
    CHANGE_INCLUDE_EP = "single şarkıları albümü indirirken ekle('0'-Hayır,'1'-Evet):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "album numarasını dosya numarsından önce değiştir('0'-Hayır ,'1'-Evet):"
    CHANGE_SAVE_COVERS = "Kapak resmini kaydet('0'-Hayır ,'1'-Evet):"
    CHANGE_LANGUAGE = "Dil seç"

    MSG_INVAILD_ACCESSTOKEN = "Hatalı AccessToken! ."
    MSG_PATH_ERR = "Indirilen dosyası hatalı!"
    MSG_INPUT_ERR = "Giriş Hatalı!"


    MODEL_ALBUM_PROPERTY = "ALBUM-MÜLKİYETI"
    MODEL_TRACK_PROPERTY = "ŞARKI-MÜLKİYETI"
    MODEL_VIDEO_PROPERTY = "VIDEO-MÜLKİYETİ"
    MODEL_ARTIST_PROPERTY = "ARTIST-MÜLKİYETI"
    MODEL_PLAYLIST_PROPERTY = "OYNATMA LİSTESİ-MÜLKİYETİ"

    MODEL_TITLE = 'İsim'
    MODEL_TRACK_NUMBER = 'şarkı numarsı'
    MODEL_VIDEO_NUMBER = 'Video numarası'
    MODEL_RELEASE_DATE = 'Çıkış Yılı'
    MODEL_VERSION = 'Versiyonu'
    MODEL_EXPLICIT = 'Açık '
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'Takip Numarası'
    MODEL_NAME = 'Isim'
    MODEL_TYPE = 'Tip'
