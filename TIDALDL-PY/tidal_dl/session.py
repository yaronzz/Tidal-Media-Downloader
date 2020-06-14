#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pickle
import uuid
import os
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs
import hashlib
import base64
import secrets
from datetime import datetime, timedelta

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from tidal_dl.tidal import TidalConfig

'''
@File    :   session.py
@Time    :   2020/06/09
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   Class from project "Redsea"
'''

class TidalMobileSession(object):
    # client_id	CLGLE93UA5gm42Og  ck3zaWMi8Ka_XdI0
    # client_id	RnhXoTmoJgARtXHr
    def __init__(self, username, password, client_id='ck3zaWMi8Ka_XdI0', cf=None):
        self.username = username
        self.client_id = client_id
        self.redirect_uri =  'https://tidal.com/android/login/auth'
        self.code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=')
        self.code_challenge = base64.urlsafe_b64encode(hashlib.sha256(self.code_verifier).digest()).rstrip(b'=')
        self.client_unique_key = secrets.token_hex(16)
        self.access_token = None
        self.user_id = None
        self.country_code = None
        self.errmsg = None

        if cf is not None and cf.username == username:
            self.user_id = cf.userid
            self.access_token = cf.accesstoken
            if self.valid():
                self.country_code = cf.countrycode
                self.password = password
                return
        self.auth(password)

    def auth(self, password):
        s = requests.Session()

        params = {
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'lang': 'en_US',
            'appMode': 'android',
            'client_id': self.client_id,
            'client_unique_key': self.client_unique_key,
            'code_challenge': self.code_challenge,
            'code_challenge_method': 'S256'
        }

        # retrieve csrf token for subsequent request
        r = s.get('https://login.tidal.com/authorize', params=params)

        # enter email, verify email is valid
        r = s.post('https://login.tidal.com/email', params=params, json={
            '_csrf': s.cookies['token'],
            'email': self.username,
            'recaptchaResponse': ''
        })
        if r.status_code != 200:
            self.errmsg = 'Unknown in https://login.tidal.com/email'
            return
        if not r.json()['isValidEmail']:
            self.errmsg = 'Invalid email'
            return
        if r.json()['newUser']:
            self.errmsg = 'User does not exist'
            return

        # login with user credentials
        r = s.post('https://login.tidal.com/email/user/existing', params=params, json={
            '_csrf': s.cookies['token'],
            'email': self.username,
            'password': password
        })
        if r.status_code != 200:
            self.errmsg = 'Unknown in https://login.tidal.com/email/user/existing'
            return

        # retrieve access code
        r = s.get('https://login.tidal.com/success?lang=en', allow_redirects=False)
        if r.status_code == 401:
            self.errmsg = 'Incorrect password'
            return
        if r.status_code != 302:
            self.errmsg = 'Unknown in https://login.tidal.com/success?lang=en'
            return
        url = urlparse.urlparse(r.headers['location'])
        oauth_code = parse_qs(url.query)['code'][0]

        # exchange access code for oauth token
        r = requests.post('https://auth.tidal.com/v1/oauth2/token', data={
            'code': oauth_code,
            'client_id': self.client_id,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'scope': 'r_usr w_usr w_sub',
            'code_verifier': self.code_verifier,
            'client_unique_key': self.client_unique_key
        })
        if r.status_code != 200:
            self.errmsg = 'Unknown in https://auth.tidal.com/v1/oauth2/token'
            return
        self.access_token = r.json()['access_token']

        r = requests.get('https://api.tidal.com/v1/sessions', headers=self.auth_headers())
        if r.status_code != 200:
            self.errmsg = 'Unknown in https://api.tidal.com/v1/sessions'
            return
        self.user_id = r.json()['userId']
        self.country_code = r.json()['countryCode']

    def valid(self):
        r = requests.get('https://api.tidal.com/v1/sessions', headers=self.auth_headers())
        return r.status_code == 200

    def auth_headers(self):
        return {'authorization': 'Bearer {}'.format(self.access_token)}

