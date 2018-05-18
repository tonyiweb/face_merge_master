# -*- coding: utf-8 -*-

import time
import random
import hmac, hashlib
import binascii
import base64
from youtu_tool import conf

class Auth(object):

    def __init__(self, secret_id, secret_key, appid, userid):
        self.AUTH_URL_FORMAT_ERROR = -1
        self.AUTH_SECRET_ID_KEY_ERROR = -2

        self._secret_id = secret_id
        self._secret_key = secret_key
        self._appid = appid
        self._userid = userid

    def app_sign(self, expired=0):
        if not self._secret_id or not self._secret_key:
            return self.AUTH_SECRET_ID_KEY_ERROR

        puserid = ''
        if self._userid != '':
            if len(self._userid) > 64:
                return self.AUTH_URL_FORMAT_ERROR
            puserid = self._userid
 
        now = int(time.time())
        rdm = random.randint(0, 999999999)
        plain_text = 'a=' + self._appid + '&k=' + self._secret_id + '&e=' + str(expired) + '&t=' + str(now) + '&r=' + str(rdm) + '&u=' + puserid + '&f=' 
        bin = hmac.new(self._secret_key.encode(), plain_text.encode(), hashlib.sha1)
        s = bin.hexdigest()
        s = binascii.unhexlify(s)
        s = s + plain_text.encode('ascii')
        signature = base64.b64encode(s).rstrip()    #生成签名
        return signature

