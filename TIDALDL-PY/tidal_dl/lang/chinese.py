#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   chinese.py
@Time    :   2020/08/19
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''

class LangChinese(object):
    SETTING = "设置"
    VALUE = "值"
    SETTING_DOWNLOAD_PATH = "下载目录"
    SETTING_ONLY_M4A = "转换mp4为m4a"
    SETTING_ADD_EXPLICIT_TAG = "文件名添加脏话标签Explicit"
    SETTING_ADD_HYPHEN = "文件名用'-'代替空格"
    SETTING_ADD_YEAR = "专辑文件夹添加年代标签"
    SETTING_USE_TRACK_NUM = "歌曲名称添加序号"
    SETTING_AUDIO_QUALITY = "歌曲质量"
    SETTING_VIDEO_QUALITY = "视频质量"
    SETTING_CHECK_EXIST = "是否跳过已下载的文件"
    SETTING_ARTIST_BEFORE_TITLE = "文件名前添加歌手名"
    SETTING_ALBUMID_BEFORE_FOLDER = "专辑文件夹添加专辑ID"
    SETTING_INCLUDE_EP = "下载歌手专辑时包含其EP单曲"
    SETTING_SAVE_COVERS = "保存封面"
    SETTING_LANGUAGE = "语言"

    CHOICE = "选项"
    FUNCTION = "功能"
    CHOICE_ENTER = "输入"
    CHOICE_ENTER_URLID = "输入 'Url或ID':"
    CHOICE_EXIT = "退出"
    CHOICE_LOGIN = "登录"
    CHOICE_SETTINGS = "配置"
    CHOICE_SET_ACCESS_TOKEN = "设置AccessToken"
    CHOICE_DOWNLOAD_BY_URL = "通过链接或ID下载"

    PRINT_ERR = "[错误]"
    PRINT_INFO = "[提示]"
    PRINT_SUCCESS = "[成功]"

    PRINT_ENTER_CHOICE = "输入选项:"
    PRINT_LATEST_VERSION = "最新版本:"
    PRINT_USERNAME = "用户:"
    PRINT_PASSWORD = "密码:"

    CHANGE_START_SETTINGS = "开始设置('0'-返回,'1'-是):"
    CHANGE_DOWNLOAD_PATH = "下载路径('0' 不修改):"
    CHANGE_AUDIO_QUALITY = "音频质量('0'-Normal,'1'-High,'2'-HiFi,'3'-Master):"
    CHANGE_VIDEO_QUALITY = "视频质量('0'-1080,'1'-720,'2'-480,'3'-360):"
    CHANGE_ONLYM4A = "将Mp4格式的音频转为M4a('0'-不,'1'-是):"
    CHANGE_ADD_EXPLICIT_TAG = "歌名后添加脏话标签('0'-不,'1'-是):"
    CHANGE_ADD_HYPHEN = "文件名中用'-'代替空格('0'-不,'1'-是):"
    CHANGE_ADD_YEAR = "专辑目录前添加年代标签('0'-不,'1'-是):"
    CHANGE_USE_TRACK_NUM = "文件名前添加序号('0'-不,'1'-是):"
    CHANGE_CHECK_EXIST = "下载前检查是否有已下载的文件('0'-不,'1'-是):"
    CHANGE_ARTIST_BEFORE_TITLE = "文件名前添加歌手名称('0'-不,'1'-是):"
    CHANGE_INCLUDE_EP = "下载歌手专辑时包含其EP单曲('0'-不,'1'-是):"
    CHANGE_ALBUMID_BEFORE_FOLDER = "专辑目录前添加ID('0'-不,'1'-是):"
    CHANGE_SAVE_COVERS = "保存封面('0'-不,'1'-是):"
    CHANGE_LANGUAGE = "选择语言"

    MSG_INVAILD_ACCESSTOKEN = "无效的 AccessToken! 请重新设置."
    MSG_PATH_ERR = "路径错误!"
    MSG_INPUT_ERR = "输入错误!"


    MODEL_ALBUM_PROPERTY = "专辑信息"
    MODEL_TRACK_PROPERTY = "歌曲信息"
    MODEL_VIDEO_PROPERTY = "视频信息"
    MODEL_ARTIST_PROPERTY = "歌手信息"
    MODEL_PLAYLIST_PROPERTY = "歌单信息"

    MODEL_TITLE = '标题'
    MODEL_TRACK_NUMBER = '歌曲数量'
    MODEL_VIDEO_NUMBER = '视频数量'
    MODEL_RELEASE_DATE = '发布时间'
    MODEL_VERSION = '版本'
    MODEL_EXPLICIT = '脏话标志'
    MODEL_ALBUM = '专辑'
    MODEL_ID = 'ID'
    MODEL_NAME = '名称'
    MODEL_TYPE = '类型'
