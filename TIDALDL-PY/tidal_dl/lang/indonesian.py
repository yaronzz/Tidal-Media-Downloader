#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   indonesian.py
@Time    :   2023/12/16
@Author  :   ErZ
@Version :   1.2
@Contact :   
@Desc    :   
'''


class LangIndonesian(object):
    SETTING = "PENGATURAN"
    VALUE = "Nilai"
    SETTING_DOWNLOAD_PATH = "Jalur unduhan"
    SETTING_ONLY_M4A = "Konversi mp4 ke m4a"
    SETTING_ADD_EXPLICIT_TAG = "Berikan tag explicit"
    SETTING_ADD_HYPHEN = "Berikan tanda hubung"
    SETTING_ADD_YEAR = "Berikan tahun sebelum berkas album"
    SETTING_USE_TRACK_NUM = "Tambahkan nomor lagu pengguna"
    SETTING_AUDIO_QUALITY = "Kualitas audio"
    SETTING_VIDEO_QUALITY = "Kualitas video"
    SETTING_CHECK_EXIST = "Periksa ada"
    SETTING_ARTIST_BEFORE_TITLE = "Nama artis sebelum nama lagu"
    SETTING_ALBUMID_BEFORE_FOLDER = "Nomor id sebelum folder album"
    SETTING_INCLUDE_EP = "Masukkan single & EP"
    SETTING_SAVE_COVERS = "Simpan sampul"
    SETTING_LANGUAGE = "Bahasa"
    SETTING_USE_PLAYLIST_FOLDER = "Gunakan folder daftar putar"
    SETTING_MULITHREAD_DOWNLOAD = "Pengunduhan multi utas"
    SETTING_ALBUM_FOLDER_FORMAT = "Format folder album"
    SETTING_PLAYLIST_FOLDER_FORMAT = "Format folder daftar putar"
    SETTING_TRACK_FILE_FORMAT = "Format berkas lagu"
    SETTING_VIDEO_FILE_FORMAT = "Format berkas video"
    SETTING_SHOW_PROGRESS = "Tampilkan progres"
    SETTING_SHOW_TRACKINFO = "Tampilkan Track Info"
    SETTING_SAVE_ALBUMINFO = "Simpan AlbumInfo.txt"
    SETTING_DOWNLOAD_VIDEOS = "Unduh video"
    SETTING_ADD_LYRICS = "Tambahkan lirik"
    SETTING_LYRICS_SERVER_PROXY = "Proksi server lirik"
    SETTING_ADD_LRC_FILE = "Simpan lirik yang waktunya diatur (file .lrc)"
    SETTING_PATH = "Jalur pengaturan"
    SETTING_APIKEY = "Dukungan  APIKey"
    SETTING_ADD_TYPE_FOLDER = "Tambahkan Tipe Folder"
    SETTING_DOWNLOAD_DELAY = "Gunakan Penundaan Unduh"

    CHOICE = "PILIH"
    FUNCTION = "FUNGSI"
    CHOICE_ENTER = "Masuk"
    CHOICE_ENTER_URLID = "Masukkan 'Url/ID':"
    CHOICE_EXIT = "Keluar"
    CHOICE_LOGIN = "Cek AccessToken"
    CHOICE_SETTINGS = "Pengaturan"
    CHOICE_SET_ACCESS_TOKEN = "Tetapkan AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Unduh dengan url atau ID"
    CHOICE_LOGOUT = "Keluar"
    CHOICE_APIKEY = "Pilih APIKey"

    PRINT_ERR = "[ERROR]"
    PRINT_INFO = "[INFORMASI]"
    PRINT_SUCCESS = "[SUKSES]"

    PRINT_ENTER_CHOICE = "Masukkan pilihan:"
    PRINT_LATEST_VERSION = "Versi terbaru:"
    # PRINT_USERNAME = "nama pengguna:"
    # PRINT_PASSWORD = "sandi:"

    CHANGE_START_SETTINGS = "Pengaturan awal('0'-Kembali,'1'-Ya):"
    CHANGE_DOWNLOAD_PATH = "Jalur unduhan('0'-Jangan ubah):"
    CHANGE_AUDIO_QUALITY = "Kualitas audio('0'-Normal,'1'-High,'2'-HiFi,'3'-Master,'4'-Max):"
    CHANGE_VIDEO_QUALITY = "Kualitas video(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Konversi mp4 ke m4a('0'-Tidak,'1'-Ya):"
    CHANGE_ADD_EXPLICIT_TAG = "Tambahkan tag eksplisit ke nama file('0'-Tidak,'1'-Ya):"
    CHANGE_ADD_HYPHEN = "Gunakan tanda hubung daripada spasi pada nama file('0'-Tidak,'1'-Ya):"
    CHANGE_ADD_YEAR = "Tambahkan tahun ke nama folder('0'-Tidak,'1'-Ya):"
    CHANGE_USE_TRACK_NUM = "Tambahkan nomor lagu sebelum nama file('0'-Tidak,'1'-Ya):"
    CHANGE_CHECK_EXIST = "Periksa file yang ada sebelum mengunduh lagu('0'-Tidak,'1'-Ya):"
    CHANGE_ARTIST_BEFORE_TITLE = "Tambahkan nama artist sebelum judul lagu('0'-Tidak,'1'-Ya):"
    CHANGE_INCLUDE_EP = "Masukkan single and EP ketika mengunduh album artis('0'-Tidak,'1'-Ya):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Berikan id sebelum folder album('0'-Tidak,'1'-Ya):"
    CHANGE_SAVE_COVERS = "Unduh sampul('0'-Tidak,'1'-Ya):"
    CHANGE_LANGUAGE = "Pilih bahasa"
    CHANGE_ALBUM_FOLDER_FORMAT = "Format folder album('0'-Jangan ubah,'default'-untuk menetapkan standar):"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Format folder daftar putar('0'-Jangan ubah,'default'-untuk menetapkan standar):"
    CHANGE_TRACK_FILE_FORMAT = "Format file lagu('0'-Jangan ubah,'default'-untuk menetapkan standar):"
    CHANGE_VIDEO_FILE_FORMAT = "Format file video('0'-Jangan ubah,'default'-untuk menetapkan standar):"
    CHANGE_SHOW_PROGRESS = "Tampilkan progres('0'-Tidak,'1'-Ya):"
    CHANGE_SHOW_TRACKINFO = "Tampilkan informasi lagu('0'-Tidak,'1'-Ya):"
    CHANGE_SAVE_ALBUM_INFO = "Unduh AlbumInfo.txt('0'-Tidak,'1'-Ya):"
    CHANGE_DOWNLOAD_VIDEOS = "Unduh video (ketika mengunduh daftar putar, album, campuran)('0'-Tidak,'1'-Ya):"
    CHANGE_ADD_LYRICS = "Tambah lirik('0'-Tidak,'1'-Ya):"
    CHANGE_LYRICS_SERVER_PROXY = "Server proksi lirik('0'-Jangan ubah):"
    CHANGE_ADD_LRC_FILE = "Simpan .lrc yang waktunya diatur('0'-Tidak,'1'-Ya):"
    CHANGE_ADD_TYPE_FOLDER = "Menambahkan Jenis-Folder, contoh Album/Video/Daftar Putar('0'-Tidak,'1'-Ya):"
    CHANGE_MULITHREAD_DOWNLOAD = "Pengunduhan multi utas('0'-Tidak,'1'-Ya):"
    CHANGE_USE_DOWNLOAD_DELAY = "Gunakan Penundaan Unduh('0'-Tidak,'1'-Ya):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Memulai proses login..."
    AUTH_LOGIN_CODE = "Kode login anda adalah {}"
    AUTH_NEXT_STEP = "Pergi ke {} sebelum {} untuk menyelesaikan penyiapan."
    AUTH_WAITING = "Menunggu otorisasi..."
    AUTH_TIMEOUT = "Waktu operasi habis."

    MSG_VALID_ACCESSTOKEN = "AccessToken baik untuk ."
    MSG_INVALID_ACCESSTOKEN = "AccessToken kedaluwarsa. Mencoba menyegarkannya kembali."
    MSG_PATH_ERR = "Jalur mengalami kesalahan!"
    MSG_INPUT_ERR = "Kesalahan input!"

    MODEL_ALBUM_PROPERTY = "PROPERTI ALBUM"
    MODEL_TRACK_PROPERTY = "PROPERTI LAGU"
    MODEL_VIDEO_PROPERTY = "PROPERTI VIDEO"
    MODEL_ARTIST_PROPERTY = "PROPERTI ARTIS"
    MODEL_PLAYLIST_PROPERTY = "PROPERTI DAFTAR PUTAR"

    MODEL_TITLE = 'Judul'
    MODEL_TRACK_NUMBER = 'Nomor Lagu'
    MODEL_VIDEO_NUMBER = 'Nomor Video'
    MODEL_RELEASE_DATE = 'Release Date'
    MODEL_VERSION = 'Versi'
    MODEL_EXPLICIT = 'Eksplisit'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Nama'
    MODEL_TYPE = 'Tipe'
