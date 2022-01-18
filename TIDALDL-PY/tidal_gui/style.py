#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :  enum.py
@Date    :  2021/05/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :  
'''

from enum import Enum


class ButtonStyle(Enum):
    Default = 0,
    Primary = 1,
    Success = 2,
    Danger = 3,
    Warning = 4,
    Info = 5,

    CloseWindow = 6,
    MaxWindow = 7,
    MinWindow = 8,

    SearchIcon = 9,
    TaskIcon = 10,
    SettingsIcon = 11,
    AboutIcon = 12,

    SoftwareIcon = 13

    PrePage = 14
    NextPage = 15

    TaskRetry = 16,
    TaskCancel = 17,
    TaskDelete = 18,
    TaskOpen = 19,
    TaskExpand = 20,


class LabelStyle(Enum):
    Default = 0,
    PageTitle = 1,
    PageSubTitle = 2,
    HugeTitle = 3,
    LogoBottom = 4,
    SearchErr = 5,
    Icon = 6,
    Bold = 7,
    Italic = 9,
    Tag = 10


class ThemeStyle(Enum):
    Default = 0,
    Dark = 1,


class ListWidgetStyle(Enum):
    Default = 0,
    TaskTab = 1,
    DownloadItems = 2,
