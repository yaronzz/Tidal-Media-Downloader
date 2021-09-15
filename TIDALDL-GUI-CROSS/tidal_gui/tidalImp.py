#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  tidalImp.py
@Date    :  2021/9/2
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import time

import requests
import tidal_dl.model
from aigpy.stringHelper import isNull
from tidal_dl import TokenSettings, TOKEN, TidalAPI


class TidalImp(TidalAPI):
    def __init__(self):
        super(TidalImp, self).__init__()

    def loginByConfig(self):
        if isNull(TOKEN.accessToken):
            return False

        msg, check = self.verifyAccessToken(TOKEN.accessToken)
        if check:
            self.key.countryCode = TOKEN.countryCode
            self.key.userId = TOKEN.userid
            self.key.accessToken = TOKEN.accessToken
            return True

        msg, check = self.refreshAccessToken(TOKEN.refreshToken)
        if check:
            TOKEN.userid = self.key.userId
            TOKEN.countryCode = self.key.countryCode
            TOKEN.accessToken = self.key.accessToken
            TOKEN.expiresAfter = time.time() + int(self.key.expiresIn)
            TokenSettings.save(TOKEN)
            return True
        else:
            tmp = TokenSettings()  # clears saved tokens
            TokenSettings.save(tmp)
            return False

    def loginByWeb(self):
        start = time.time()
        elapsed = 0
        while elapsed < self.key.authCheckTimeout:
            elapsed = time.time() - start
            msg, check = self.checkAuthStatus()
            if not check:
                if msg == "pending":
                    time.sleep(self.key.authCheckInterval + 1)
                    continue
                return False
            if check:
                TOKEN.userid = self.key.userId
                TOKEN.countryCode = self.key.countryCode
                TOKEN.accessToken = self.key.accessToken
                TOKEN.refreshToken = self.key.refreshToken
                TOKEN.expiresAfter = time.time() + int(self.key.expiresIn)
                TokenSettings.save(TOKEN)
                return True
        return False

    @staticmethod
    def getArtistsNames(self, artists: list[tidal_dl.model.Artist]):
        ret = []
        for item in artists:
            ret.append(item.name)
        return ','.join(ret)

    @staticmethod
    def getDurationString(seconds: int):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def getCoverData(self, sid, width="320", height="320"):
        url = self.getCoverUrl(sid, width, height)
        try:
            respond = requests.get(url)
            return respond.content
        except:
            return ''


tidalImp = TidalImp()
