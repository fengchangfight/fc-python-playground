# -*- coding: utf-8 -*-
import requests
from urllib.parse import urlencode
import hashlib
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


class Translator(object):
    def cust_md5(self, st):
        hash_md5 = hashlib.md5(st)
        return hash_md5.hexdigest()

    def get_current_milli(self):
        d = datetime.now()
        return str(d.microsecond / 1000 + d.second * 1000)


    def baidu_translate(self, sentence):
        appid = "**"
        secret = "**"
        salt = self.get_current_milli()
        beforeMD5 = appid + sentence + salt + secret;
        sign = self.cust_md5(beforeMD5);
        params = {"q": sentence, "from": "en", "to": "zh", "appid": appid, "salt": salt, "sign": sign}
        base_url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
        request_url = base_url + "?" + urlencode(params)
        r = requests.get(request_url, headers=headers)
        print(r.content.decode('unicode-escape').encode('utf-8'))
        return r.content


s = "I love you"
trans = Translator()
trans.baidu_translate(s)