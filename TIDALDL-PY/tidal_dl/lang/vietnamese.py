#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   vietnamese.py
@Time    :   2020/11/12
@Author  :   MinhNgo
@Version :   1.0
@Contact :   iam.minhnc@outlook.com
@Desc    :   
'''

class LangVietnamese(object):
    SETTING = "THIẾT LẬP"
    VALUE = "GIÁ TRỊ"
    SETTING_DOWNLOAD_PATH = "Đường dẫn tải về"
    SETTING_ONLY_M4A = "Đổi mp4 qua m4a"
    SETTING_ADD_EXPLICIT_TAG = "Thêm tag explicit"
    SETTING_ADD_HYPHEN = "Thêm dấu nối"
    SETTING_ADD_YEAR = "Thêm năm trước thư mục album"
    SETTING_USE_TRACK_NUM = "Thêm STT track"
    SETTING_AUDIO_QUALITY = "Chất lượng âm thanh"
    SETTING_VIDEO_QUALITY = "Chất lượng video"
    SETTING_CHECK_EXIST = "Kiểm tra tồn tại"
    SETTING_ARTIST_BEFORE_TITLE = "Tên nghệ sĩ phía trước tựa bài hát"
    SETTING_ALBUMID_BEFORE_FOLDER = "Id trước thư mục album"
    SETTING_INCLUDE_EP = "Bao gồm đĩa đơn & ep"
    SETTING_SAVE_COVERS = "Tải ảnh bìa"
    SETTING_LANGUAGE = "Ngôn ngữ"
    SETTING_USE_PLAYLIST_FOLDER = "Thư mục cho danh sách phát"
    SETTING_MULITHREAD_DOWNLOAD = "Tải về đa luồng"
    SETTING_ALBUM_FOLDER_FORMAT = "Định dạng thư mục album"
    SETTING_TRACK_FILE_FORMAT = "Định dạng tên tệp nhạc"
    SETTING_SHOW_PROGRESS = "Hiện tiến trình"

    CHOICE = "LỰA CHỌN"
    FUNCTION = "CHỨC NĂNG"
    CHOICE_ENTER = "Nhập"
    CHOICE_ENTER_URLID = "Nhập 'Url/ID':"
    CHOICE_EXIT = "Thoát"
    CHOICE_LOGIN = "Kiểm tra AccessToken"
    CHOICE_SETTINGS = "Thiết lập"
    #CHOICE_SET_ACCESS_TOKEN = "Nhập AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "Tải về qua url hoặc id"
    CHOICE_LOGOUT = "Logout"

    PRINT_ERR = "[LỖI]"
    PRINT_INFO = "[INFO]"
    PRINT_SUCCESS = "[XONG]"

    PRINT_ENTER_CHOICE = "Nhập lựa chọn:"
    PRINT_LATEST_VERSION = "Bản mới nhất:"
    #PRINT_USERNAME = "tên đăng nhập:"
    #PRINT_PASSWORD = "mật khẩu:"
    
    CHANGE_START_SETTINGS = "Bắt đầu thiết lập('0'-Về,'1'-Có):"
    CHANGE_DOWNLOAD_PATH = "Đường dẫn tải về('0' không đổi):"
    CHANGE_AUDIO_QUALITY = "Chất lượng âm thanh('0'-Normal,'1'-High,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "Chất lượng video('0'-1080,'1'-720,'2'-480,'3'-360):"
    CHANGE_ONLYM4A = "Đổi mp4 qua m4a('0'-Không,'1'-Có):"
    CHANGE_ADD_EXPLICIT_TAG = "Thêm tag explicit vào tên tệp('0'-Không,'1'-Có):"
    CHANGE_ADD_HYPHEN = "Dùng gạch nối thay vì spaces trong tên tệp('0'-Không,'1'-Có):"
    CHANGE_ADD_YEAR = "Thêm năm phía trước tên thư mục album('0'-Không,'1'-Có):"
    CHANGE_USE_TRACK_NUM = "Thêm STT track đầu tên tệp('0'-Không,'1'-Có):"
    CHANGE_CHECK_EXIST = "Kiểm tra tệp đã tồn tại chưa trước khi tải('0'-Không,'1'-Có):"
    CHANGE_ARTIST_BEFORE_TITLE = "Thêm tên nghệ sĩ trước tựa đề('0'-Không,'1'-Có):"
    CHANGE_INCLUDE_EP = "Bao gồm đĩa đơn và EPs khi tải tất cả nhạc của nghệ sĩ('0'-Không,'1'-Có):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "Thêm id phía trước tên thư mục album('0'-Không,'1'-Có):"
    CHANGE_SAVE_COVERS = "Tải ảnh bìa('0'-Không,'1'-Có):"
    CHANGE_LANGUAGE = "Chọn ngôn ngữ"
    CHANGE_ALBUM_FOLDER_FORMAT = "Định dạng thư mục album('0' không đổi):"
    CHANGE_TRACK_FILE_FORMAT = "Định dạng tên tệp nhạc('0' không đổi):"
    CHANGE_SHOW_PROGRESS = "Hiện tiến trình('0'-Không,'1'-Có):"

    # {} are required in these strings
    AUTH_START_LOGIN = "Đang bắt đầu đăng nhập..."
    AUTH_LOGIN_CODE = "Mã đăng nhập của bạn là {}"
    AUTH_NEXT_STEP = "Vào trang {} trong vòng {} để hoàn tất thiết lập."
    AUTH_WAITING = "Đang chờ xác minh..."
    AUTH_TIMEOUT = "Đã vượt quá thời gian chờ."
    
    MSG_VALID_ACCESSTOKEN = "AccessToken vẫn tốt trong {}."
    MSG_INVAILD_ACCESSTOKEN = "AccessToken hết hạn. Đang cố gắng làm mới."
    MSG_PATH_ERR = "Lỗi đường dẫn!"
    MSG_INPUT_ERR = "Lỗi nhập!"

    MODEL_ALBUM_PROPERTY = "THÔNG TIN ALBUM"
    MODEL_TRACK_PROPERTY = "THÔNG TIN TRACK"
    MODEL_VIDEO_PROPERTY = "THÔNG TIN VIDEO"
    MODEL_ARTIST_PROPERTY = "THÔNG TIN NGHỆ SĨ"
    MODEL_PLAYLIST_PROPERTY = "THÔNG TIN PLAYLIST"

    MODEL_TITLE = 'Tựa đề'
    MODEL_TRACK_NUMBER = 'Số Track'
    MODEL_VIDEO_NUMBER = 'Số Video'
    MODEL_RELEASE_DATE = 'Ngày phát hành'
    MODEL_VERSION = 'Phiên bản'
    MODEL_EXPLICIT = 'Explicit'
    MODEL_ALBUM = 'Album'
    MODEL_ID = 'ID'
    MODEL_NAME = 'Tên'
    MODEL_TYPE = 'Loại'
