#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   malay.py
@Time    :   2023/12/17
@Author  :   ErZ
@Version :   1.2
@Contact :   
@Desc    :   
'''


class LangMalay(object):
    SETTING = "SETING"
    VALUE = "Nilai"
    SETTING_DOWNLOAD_PATH = "Laluan muat"
    SETTING_ONLY_M4A = "Tukar mp4 kepada m4a"
    SETTING_ADD_EXPLICIT_TAG = "Tambah tag explicit"
    SETTING_ADD_HYPHEN = "Tambah tanda sempang"
    SETTING_ADD_YEAR = "Tambah tahun sebelum album-folder"
    SETTING_USE_TRACK_NUM = "Tambah Nombor trek pengguna"
    SETTING_AUDIO_QUALITY = "Kualiti audio"
    SETTING_VIDEO_QUALITY = "Kualiti video"
    SETTING_CHECK_EXIST = "Periksa wujud"
    SETTING_ARTIST_BEFORE_TITLE = "ArtistName sebelum tajuk lagu"
    SETTING_ALBUMID_BEFORE_FOLDER = "Id sebelum album-folder"
    SETTING_INCLUDE_EP = "Termasuk singles & EPs"
    SETTING_SAVE_COVERS = "Simpan penutup"
    SETTING_LANGUAGE = "Bahasa"
    SETTING_USE_PLAYLIST_FOLDER = "Gunakan folder senarai main"
    SETTING_MULITHREAD_DOWNLOAD = "Muat berbilang benang"
    SETTING_ALBUM_FOLDER_FORMAT = "Format folder album"
    SETTING_PLAYLIST_FOLDER_FORMAT = "Format folder senarai main"
    SETTING_TRACK_FILE_FORMAT = "Format fail audio"
    SETTING_VIDEO_FILE_FORMAT = "Format fail video"
    SETTING_SHOW_PROGRESS = "Tunjukkan perkembangan"
    SETTING_SHOW_TRACKINFO = "Tunjukkan info trek"
    SETTING_SAVE_ALBUMINFO = "Save AlbumInfo.txt"
    SETTING_DOWNLOAD_VIDEOS = "Simpan AlbumInfo.txt"
    SETTING_ADD_LYRICS = "Tambah lirik"
    SETTING_LYRICS_SERVER_PROXY = "Proksi pelayan lirik"
    SETTING_ADD_LRC_FILE = "Simpan lirik tepat pada masanya (fail .lrc)"
    SETTING_PATH = "Seting laluan"
    SETTING_APIKEY = "Sokongan APIKey"
    SETTING_ADD_TYPE_FOLDER = "Tambah Taip Folder"
    SETTING_DOWNLOAD_DELAY = "Gunakan Muat Berlengah"

    CHOICE = "PILIH"
    FUNCTION = "FUNGSI"
    CHOICE_ENTER = "Masukkan"
    CHOICE_ENTER_URLID = "Masukkan 'Url/ID':"
    CHOICE_EXIT = "Keluar"
    CHOICE_LOGIN = "Periksa AccessToken"
    CHOICE_SETTINGS = "Seting"
    CHOICE_SET_ACCESS_TOKEN = "Tetapkan AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Muat mengikut url atau ID"
    CHOICE_LOGOUT = "Keluar"
    CHOICE_APIKEY = "Pilih APIKey"

    PRINT_ERR = "[SILAP]"
    PRINT_INFO = "[MAKLUMAT]"
    PRINT_SUCCESS = "[SUKSES]"

    PRINT_ENTER_CHOICE = "Masukkan Pilihan:"
    PRINT_LATEST_VERSION = "Versi terbaru:"
    # PRINT_USERNAME = "nama pengguna:"
    # PRINT_PASSWORD = "Kata laluan:"

    CHANGE_START_SETTINGS = "Seting Mula('0'-Kembali,'1'-Ya):"
    CHANGE_DOWNLOAD_PATH = "Laluan muat('0'-Jangan ubah):"
    CHANGE_AUDIO_QUALITY = "Kualiti audio('0'-Normal,'1'-High,'2'-HiFi,'3'-Master,'4'-Max):"
    CHANGE_VIDEO_QUALITY = "Kualiti video(1080, 720, 480, 360):"
    CHANGE_ONLYM4A = "Tukar mp4 kepada m4a('0'-Tidak,'1'-Ya):"
    CHANGE_ADD_EXPLICIT_TAG = "Tambah tag eksplisit pada nama fail('0'-Tidak,'1'-Ya):"
    CHANGE_ADD_HYPHEN = "Gunakan tanda sempang dan bukannya ruang dalam nama fail('0'-Tidak,'1'-Ya):"
    CHANGE_ADD_YEAR = "Tambah tahun kepada nama folder album('0'-Tidak,'1'-Ya):"
    CHANGE_USE_TRACK_NUM = "Tambah nombor trek sebelum nama fail('0'-Tidak,'1'-Ya):"
    CHANGE_CHECK_EXIST = "Periksa fail sedia ada sebelum muat trek('0'-Tidak,'1'-Ya):"
    CHANGE_ARTIST_BEFORE_TITLE = "Tambah nama artis sebelum tajuk jejak('0'-Tidak,'1'-Ya):"
    CHANGE_INCLUDE_EP = "Sertakan single dan EPs semasa memuat album artis('0'-Tidak,'1'-Ya):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Tambah id sebelum folder album('0'-Tidak,'1'-Ya):"
    CHANGE_SAVE_COVERS = "Simpan penutup('0'-Tidak,'1'-Ya):"
    CHANGE_LANGUAGE = "Pilih bahasa"
    CHANGE_ALBUM_FOLDER_FORMAT = "Format folder album('0'-Jangan ubah,'default'-untuk mengesetkan lalai):"
    CHANGE_PLAYLIST_FOLDER_FORMAT = "Format folder senarai main('0'-Jangan ubah,'default'-untuk mengesetkan lalai):"
    CHANGE_TRACK_FILE_FORMAT = "Format fail trek('0'-Jangan ubah,'default'-untuk mengesetkan lalai):"
    CHANGE_VIDEO_FILE_FORMAT = "Video file format('0'-Jangan ubah,'default'-untuk mengesetkan lalai):"
    CHANGE_SHOW_PROGRESS = "Show progress('0'-Tidak,'1'-Ya):"
    CHANGE_SHOW_TRACKINFO = "Tunjukkan maklumat trek('0'-Tidak,'1'-Ya):"
    CHANGE_SAVE_ALBUM_INFO = "Simpan AlbumInfo.txt('0'-Tidak,'1'-Ya):"
    CHANGE_DOWNLOAD_VIDEOS = "Muat video (semasa memuat senarai main, album, campuran)('0'-Tidak,'1'-Ya):"
    CHANGE_ADD_LYRICS = "Tambah lirik('0'-Tidak,'1'-Ya):"
    CHANGE_LYRICS_SERVER_PROXY = "Proksi pelayan lirik('0'-Jangan ubah):"
    CHANGE_ADD_LRC_FILE = "Simpan lirik tepat pada masanya .lrc fail ('0'-Tidak,'1'-Ya):"
    CHANGE_ADD_TYPE_FOLDER = "Tambah Taip Folder,contohnya Album/Video/Senarai Main('0'-Tidak,'1'-Ya):"
    CHANGE_MULITHREAD_DOWNLOAD = "Multi thread download('0'-Tidak,'1'-Ya):"
    CHANGE_USE_DOWNLOAD_DELAY = "Gunakan Muat Berlengah('0'-Tidak,'1'-Ya):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Memulakan proses masuk..."
    AUTH_LOGIN_CODE = "Kod masuk anda ialah {}"
    AUTH_NEXT_STEP = "Pergi ke {} dalam {} untuk melengkapkan pemasangan."
    AUTH_WAITING = "Menunggu authorization..."
    AUTH_TIMEOUT = "Operasi tamat masa."

    MSG_VALID_ACCESSTOKEN = "AccessToken baik untuk {}."
    MSG_INVALID_ACCESSTOKEN = "AccessToken yang telah tamat tempoh. Cuba menyegar semulanya."
    MSG_PATH_ERR = "Laluan adalah kesilapan!"
    MSG_INPUT_ERR = "Silap input!"

    MODEL_ALBUM_PROPERTY = "HARTANAH ALBUM"
    MODEL_TRACK_PROPERTY = "HARTANAH TREK"
    MODEL_VIDEO_PROPERTY = "HARTANAH VIDEO"
    MODEL_ARTIST_PROPERTY = "HARTANAH ARTIS"
    MODEL_PLAYLIST_PROPERTY = "HARTANAH SENARAI MAIN"

    MODEL_TITLE = 'Tajuk'
    MODEL_TRACK_NUMBER = 'Nombor trek'
    MODEL_VIDEO_NUMBER = 'Nombor video'
    MODEL_RELEASE_DATE = 'Tarikh Keluar'
    MODEL_VERSION = 'Versi'
    MODEL_EXPLICIT = 'Eksplisit'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Nama'
    MODEL_TYPE = 'Taip'
