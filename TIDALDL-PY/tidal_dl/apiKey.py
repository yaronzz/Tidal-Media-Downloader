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
import json
import requests

__KEYS_JSON__ = '''
{
    "version": "1.0.1",
    "keys": [
        {
            "platform": "Android Auto",
            "formats": "Normal/High/HiFi/Master",
            "clientId": "zU4XHVVkc2tDPo4t",
            "clientSecret": "VJKhDFqJPqvsPVNBV6ukXTJmwlvbttP7wlMlrc72se4=",
            "valid": "True",
            "from": "1nikolas (https://github.com/yaronzz/Tidal-Media-Downloader/pull/840)"
        },
        {
            "platform": "Fire TV",
            "formats": "Master-Only(Else Error)",
            "clientId": "7m7Ap0JC9j1cOM3n",
            "clientSecret": "vRAdA108tlvkJpTsGZS8rGZ7xTlbJ0qaZ2K9saEzsgY=",
            "valid": "True",
            "from": "Dniel97 (https://github.com/Dniel97/RedSea/blob/4ba02b88cee33aeb735725cb854be6c66ff372d4/config/settings.example.py#L68)"
        }
    ]
}
'''
__API_KEYS__ = json.loads(__KEYS_JSON__)
__ERROR_KEY__ = {
                    'platform': 'None',
                    'formats': '',
                    'clientId': '',
                    'clientSecret': '',
                    'valid': 'False',
                },



def getNum():
    return len(__API_KEYS__['keys'])


def getItem(index: int):
    if index < 0 or index >= len(__API_KEYS__['keys']):
        return __ERROR_KEY__
    return __API_KEYS__['keys'][index]


def getItems():
    return __API_KEYS__['keys']


def getLimitIndexs():
    array = []
    for i in range(len(__API_KEYS__['keys'])):
        array.append(str(i))
    return array


def getVersion():
    return __API_KEYS__['version']

#Load from gist
try:
    respond = requests.get('https://api.github.com/gists/48d01f5a24b4b7b37f19443977c22cd6')
    if respond.status_code == 200:
        content = respond.json()['files']['tidal-api-key.json']['content']
        __API_KEYS__ = json.loads(content)
except:
    pass


