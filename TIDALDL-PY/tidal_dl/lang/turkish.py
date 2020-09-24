#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   turkish.py
@Time    :   2020/09/13
@Author  :   Gorgeous & shhade for hack
@Version :   1.0
@Contact :   realmutlusen@gmail.com
@Desc    :   
'''

class LangTurkish(object):
    SETTING = "AYARLAR"
    VALUE = "SEÇİMLER"
    SETTING_DOWNLOAD_PATH = "İndirme Konumu:"
    SETTING_ONLY_M4A = ".mp4'ü m4a'ya çevrilsin mi?"
    SETTING_ADD_EXPLICIT_TAG = "'Explicit' yani 'küfürlü' etiketi eklensin mi?"
    SETTING_ADD_HYPHEN = "Şarkı dosyasının isminde boşluk yerine '-' eklensin mi ?"
    SETTING_ADD_YEAR = "Albüm klasörünün isminde yıl olsun mu ?"
    SETTING_USE_TRACK_NUM = "Artist numarası eklensin mi?"
    SETTING_AUDIO_QUALITY = "Ses Kalitesi:"
    SETTING_VIDEO_QUALITY = "Video Kalitesi:"
    SETTING_CHECK_EXIST = "Dosya daha önce indirilmiş mi diye kontrol edilsin mi ?"
    SETTING_ARTIST_BEFORE_TITLE = "Şarkı dosyasının ismine sanatçının adı eklensin mi?"
    SETTING_ALBUMID_BEFORE_FOLDER = "Albüm klasörünün ismine ID eklensin mi ?"
    SETTING_INCLUDE_EP = "Single'leri ve EP'leri dahil et"
    SETTING_SAVE_COVERS = "Albüm kapağını indir"
    SETTING_LANGUAGE = "Lisan"

    CHOICE = "Seçim"
    FUNCTION = "Fonksiyon"
    CHOICE_ENTER = "Enter"
    CHOICE_ENTER_URLID = "'Url/ID' Gir:"
    CHOICE_EXIT = "Çıkış"
    CHOICE_LOGIN = "Giriş Yap"
    CHOICE_SETTINGS = "Ayarlar"
    CHOICE_SET_ACCESS_TOKEN = "'AccessToken' Gir"
    CHOICE_DOWNLOAD_BY_URL = "URL ya da ID ile indir"

    PRINT_ERR = "[HATA OLUŞTU]"
    PRINT_INFO = "[BİLGİ]"
    PRINT_SUCCESS = "[İNDİRİLDİ]"

    PRINT_ENTER_CHOICE = "Seçim Gir:"
    PRINT_LATEST_VERSION = "Son Sürüm:"
    PRINT_USERNAME = "Kullanıcı Adı ya da Mail Adresi:"
    PRINT_PASSWORD = "Şifre:"
    
    CHANGE_START_SETTINGS = "Ayarları düzeltmek istediğine emin misin ?('0'-Geri Dön,'1'-Evet):"
    CHANGE_DOWNLOAD_PATH = "İndirme Konumu('0' aynı kalsın):"
    CHANGE_AUDIO_QUALITY = "Ses Kalitesi ('0'-Hayırrmal,'1'-High,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Video Kalitesi ('0'-1080,'1'-720,'2'-480,'3'-360):"
    CHANGE_ONLYM4A = ".mp4 uzantılı dosyalar m4a'ya çevrilsin mi?('0'-Hayır,'1'-Evet):"
    CHANGE_ADD_EXPLICIT_TAG = "'Explicit' yani 'küfürlü' etiketi eklensin mi?('0'-Hayır,'1'-Evet):"
    CHANGE_ADD_HYPHEN = "Şarkı dosyasının isminde boşluk yerine '-' eklensin mi ?('0'-Hayır,'1'-Evet):"
    CHANGE_ADD_YEAR = "Albüm klasörünün isminde yıl olsun mu ?('0'-Hayır,'1'-Evet):"
    CHANGE_USE_TRACK_NUM = "Şarkı dosyasının isminde albümdeki sırası yazsın mı ?('0'-Hayır,'1'-Evet):"
    CHANGE_CHECK_EXIST = "Dosya daha önce indirilmiş mi diye kontrol edilsin mi ?('0'-Hayır,'1'-Evet):"
    CHANGE_ARTIST_BEFORE_TITLE = "Şarkı dosyasının ismine sanatçının adı eklensin mi?('0'-Hayır,'1'-Evet):"
    CHANGE_INCLUDE_EP = "Artist'in tüm albümlerini indirirken Single'leri ve EP'leri de dahil edilsin mi ?('0'-Hayır,'1'-Evet):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Albüm klasörünün ismine ID eklensin mi ?('0'-Hayır,'1'-Evet):"
    CHANGE_SAVE_COVERS = "Albüm kapağı indirilsin mi?('0'-Hayır,'1'-Evet):"
    CHANGE_LANGUAGE = "Lisan Seç"

    MSG_INVAILD_ACCESSTOKEN = "Geçersiz AccessToken! Değiştiriniz."
    MSG_PATH_ERR = "İndirme konumu ile alakalı bir sorun var!"
    MSG_INPUT_ERR = "Giriş Hatalı!"


    MODEL_ALBUM_PROPERTY = "ALBÜM-BİLGİLERİ"
    MODEL_TRACK_PROPERTY = "ŞARKI-BİLGİLERİ"
    MODEL_VIDEO_PROPERTY = "VİDEO-BİLGİLERİ"
    MODEL_ARTIST_PROPERTY = "ARTİST-BİLGİLERİ"
    MODEL_PLAYLIST_PROPERTY = "OYNATMA LİSTESİ-BİLGİLERİ"

    MODEL_TITLE = 'Şarkı/Albüm Adı:'
    MODEL_TRACK_NUMBER = 'Şarkı Sayısı'
    MODEL_VIDEO_NUMBER = 'Video Sayısı'
    MODEL_RELEASE_DATE = 'Çıkış Yılı:'
    MODEL_VERSION = 'Versiyon'
    MODEL_EXPLICIT = 'Küfürlü'
    MODEL_ALBUM = 'Albüm'
    MODEL_ID = 'ID'
    MODEL_NAME = 'İsim'
    MODEL_TYPE = 'Türü'