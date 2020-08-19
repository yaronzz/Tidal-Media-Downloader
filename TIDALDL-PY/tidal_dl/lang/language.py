#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   language.py
@Time    :   2020/08/19
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
from tidal_dl.lang.english import LangEnglish
from tidal_dl.lang.chinese import LangChinese


def initLang(index):  # 初始化
    global LANG
    return setLang(index)

def setLang(index):
    global LANG
    if str(index) == '0':
        LANG = LangEnglish()
    elif str(index) == '1':
        LANG = LangChinese()
    else:
        LANG = LangEnglish()
    return LANG

def getLang():
    global LANG
    return LANG

def getLangName(index):
    if str(index) == '0':
        return "English"
    if str(index) == '1':
        return "中文"
    return "English"
