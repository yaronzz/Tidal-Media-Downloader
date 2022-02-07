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
    #api key from @Fokka-Engineering
    #https://github.com/Fokka-Engineering/libopenTIDAL/blob/655528e26e4f3ee2c426c06ea5b8440cf27abc4a/README.md#example
    {
        'platform': 'Fire TV',
        'formats': 'Normal/High/HiFi(No Master)',
        'clientId': 'OmDtrzFgyVVL6uW56OnFA2COiabqm',
        'clientSecret': 'zxen1r3pO0hgtOC7j6twMo9UAqngGrmRiWpV7QC1zJ8=',
        'valid': 'False',
    },
    #api key from @Dniel97
    #https://github.com/Dniel97/RedSea/blob/4ba02b88cee33aeb735725cb854be6c66ff372d4/config/settings.example.py#L68
    {
        'platform': 'Fire TV',
        'formats': 'Master-Only(Else Error)',
        'clientId': '7m7Ap0JC9j1cOM3n',
        'clientSecret': 'vRAdA108tlvkJpTsGZS8rGZ7xTlbJ0qaZ2K9saEzsgY=',
        'valid': 'True',
    },
    {
        'platform': 'Android TV',
        'formats': 'Normal/High/HiFi(No Master)',
        'clientId': 'Pzd0ExNVHkyZLiYN',
        'clientSecret': 'W7X6UvBaho+XOi1MUeCX6ewv2zTdSOV3Y7qC3p3675I=',
        'valid': 'False',
    },
    #api key from @morguldir 
    #https://github.com/morguldir/python-tidal/commit/50f1afcd2079efb2b4cf694ef5a7d67fdf619d09
    {
        'platform': 'TV',
        'formats': 'Normal/High/HiFi/Master',
        'clientId': '8SEZWa4J1NVC5U5Y',
        'clientSecret': 'owUYDkxddz+9FpvGX24DlxECNtFEMBxipU0lBfrbq60=',
        'valid': 'False',
    },
    {
        'platform': 'Android Auto',
        'formats': 'Normal/High/HiFi/Master',
        'clientId': 'zU4XHVVkc2tDPo4t',
        'clientSecret': 'VJKhDFqJPqvsPVNBV6ukXTJmwlvbttP7wlMlrc72se4=',
        'valid': 'True',
    },
    
]

__ERROR_KEY__ = {
                    'platform': 'None',
                    'formats': '',
                    'clientId': '',
                    'clientSecret': '',
                    'valid': 'False',
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
