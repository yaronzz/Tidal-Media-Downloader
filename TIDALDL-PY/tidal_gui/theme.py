#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  qssParse.py
@Date    :  2021/05/08
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""

import os

import aigpy

from tidal_gui.style import ThemeStyle

_RESOURCE_PATH = './resource'
if os.path.isdir(_RESOURCE_PATH):
    _RESOURCE_PATH = os.path.abspath(_RESOURCE_PATH).replace('\\', '/')
else:
    _RESOURCE_PATH = aigpy.path.getDirName(__file__).replace('\\', '/') + "resource"


def __getParam__(line: str):
    key = aigpy.string.getSub(line, "--", ":")
    value = aigpy.string.getSub(line, ":", ";")
    return key, value


def __parseParamsList__(content: str) -> dict:
    globalStr = aigpy.string.getSub(content, ":root", "}")
    lines = globalStr.split("\n")

    array = {}
    for line in lines:
        key, value = __getParam__(line)
        if key == "" or value == "":
            continue
        array[key] = value
    return array


def __parseQss__(content: str, params: dict) -> str:
    content = aigpy.string.getSub(content, "/* #QSS_START  */")
    for key in params:
        content = content.replace("var(--" + key + ")", params[key])

    content = content.replace("$RESOURCE_PATH$", _RESOURCE_PATH)
    return content


def __getQss__(filePath: str) -> str:
    content = aigpy.file.getContent(filePath)
    params = __parseParamsList__(content)
    qss = __parseQss__(content, params)
    return qss


def getResourcePath():
    return _RESOURCE_PATH


def getThemeQssContent(style: ThemeStyle = ThemeStyle.Default):
    name = "theme" + style.name + ".qss"
    return __getQss__(_RESOURCE_PATH + '/' + name)
