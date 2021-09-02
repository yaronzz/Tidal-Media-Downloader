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

import aigpy

from tidal_gui.style import ThemeStyle


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

    content = content.replace("$PACKAGE_PATH$", getPackagePath())
    return content


def __getQss__(filePath: str) -> str:
    content = aigpy.file.getContent(filePath)
    params = __parseParamsList__(content)
    qss = __parseQss__(content, params)
    return qss


def getPackagePath():
    path = __file__
    return aigpy.path.getDirName(path).replace('\\', '/')


def getThemeQssContent(style: ThemeStyle = ThemeStyle.Default):
    name = "theme" + style.name + ".qss"
    path = getPackagePath() + "/resource/"
    return __getQss__(path + name)
