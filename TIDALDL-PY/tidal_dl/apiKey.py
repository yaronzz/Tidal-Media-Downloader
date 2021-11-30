#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  apiKey.py
@Date    :  2021/11/30
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""

__API_KEYS__ = [
    {
        'platform': 'Fire TV',
        'formats': 'Normal/High/HiFi(No Master)',
        'clientId': 'OmDtrzFgyVVL6uW56OnFA2COiabqm',
        'clientSecret': 'zxen1r3pO0hgtOC7j6twMo9UAqngGrmRiWpV7QC1zJ8=',
    },
    {
        'platform': 'Fire TV',
        'formats': 'Master-Only(Else Error)',
        'clientId': '7m7Ap0JC9j1cOM3n',
        'clientSecret': 'vRAdA108tlvkJpTsGZS8rGZ7xTlbJ0qaZ2K9saEzsgY=',
    },
    {
        'platform': 'Android TV',
        'formats': 'Normal/High/HiFi(No Master)',
        'clientId': 'Pzd0ExNVHkyZLiYN',
        'clientSecret': 'W7X6UvBaho+XOi1MUeCX6ewv2zTdSOV3Y7qC3p3675I=',
    },
]

__ERROR_KEY__ = {
                    'platform': 'None',
                    'formats': '',
                    'clientId': '',
                    'clientSecret': '',
                },


def getNum():
    return len(__API_KEYS__)


def getItem(index: int):
    if index < 0 or index >= len(__API_KEYS__):
        return __ERROR_KEY__
    return __API_KEYS__[index]


def getItems():
    return __API_KEYS__


def getLimitIndexs():
    array = []
    for i in range(len(__API_KEYS__)):
        array.append(str(i))
    return array
