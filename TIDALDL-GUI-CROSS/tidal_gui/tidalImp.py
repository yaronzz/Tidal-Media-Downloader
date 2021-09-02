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


tidalImp = TidalImp()
