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

from tidal_dl.lang.arabic import LangArabic
from tidal_dl.lang.chinese import LangChinese
from tidal_dl.lang.croatian import LangCroatian
from tidal_dl.lang.czech import LangCzech
from tidal_dl.lang.danish import LangDanish
from tidal_dl.lang.dutch import LangDutch
from tidal_dl.lang.english import LangEnglish
from tidal_dl.lang.filipino import LangFilipino
from tidal_dl.lang.french import LangFrench
from tidal_dl.lang.german import LangGerman
from tidal_dl.lang.hungarian import LangHungarian
from tidal_dl.lang.italian import LangItalian
from tidal_dl.lang.norwegian import LangNorwegian
from tidal_dl.lang.polish import LangPolish
from tidal_dl.lang.portuguese import LangPortuguese
from tidal_dl.lang.russian import LangRussian
from tidal_dl.lang.spanish import LangSpanish
from tidal_dl.lang.turkish import LangTurkish
from tidal_dl.lang.ukrainian import LangUkrainian
from tidal_dl.lang.vietnamese import LangVietnamese
from tidal_dl.lang.korean import LangKorean
from tidal_dl.lang.japanese import LangJapanese

_ALL_LANGUAGE_ = [
    ['English', LangEnglish()],
    ['中文', LangChinese()],
    ['Turkish', LangTurkish()],
    ['Italian', LangItalian()],
    ['Czech', LangCzech()],
    ['Arabic', LangArabic()],
    ['Russian', LangRussian()],
    ['Filipino', LangFilipino()],
    ['Croatian', LangCroatian()],
    ['Spanish', LangSpanish()],
    ['Portuguese', LangPortuguese()],
    ['Ukrainian', LangUkrainian()],
    ['Vietnamese', LangVietnamese()],
    ['French', LangFrench()],
    ['German', LangGerman()],
    ['Danish', LangDanish()],
    ['Hungarian', LangHungarian()],
    ['Korean', LangKorean()],
    ['Japanese', LangJapanese()],
    ['Dutch', LangDutch()],
    ['Polish', LangPolish()],
    ['Norwegian', LangNorwegian()],
]

class Language(object):
    def __init__(self) -> None:
        self.select = LangEnglish()

    def __toInt__(self, str):
        try:
            return int(str)
        except:
            return 0
    
    def setLang(self, index):
        index = self.__toInt__(index)
        if index >= 0 and index < len(_ALL_LANGUAGE_):
            self.select = _ALL_LANGUAGE_[index][1]
        else:
            self.select = LangEnglish()

    def getLangName(self, index):
        index = self.__toInt__(index)
        if index >= 0 and index < len(_ALL_LANGUAGE_):
            return _ALL_LANGUAGE_[index][0]
        return ""

    def getLangChoicePrint(self):
        array = []
        index = 0
        while True:
            name = self.getLangName(index)
            if name == "":
                break
            array.append('\'' + str(index) + '\'-' + name)
            index += 1
        return ','.join(array)


LANG = Language()
