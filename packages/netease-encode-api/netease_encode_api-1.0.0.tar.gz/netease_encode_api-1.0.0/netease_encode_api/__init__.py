"""
netease_encode_api/__init__.py
Version: 1.0.0
Author: CooooldWind_
E-Mail: 3091868003@qq.com
Copyright @CooooldWind_ / Following GNU_AGPLV3+ License
"""

import json
import random
from base64 import b64encode
import requests
from Crypto.Cipher import AES
from netease_encode_api.global_args import GlobalArgs


class EncodeSession:
    """
    WeAPI解码类
    """

    def __init__(self):
        self.__global = GlobalArgs()
        self.__encode_arg_g = "0CoJUm6Qyw8W8jud"
        self.__encode_arg_i = "vlgPRPyGhwA6F4Sq"
        self.__encode_sec_key = self.__global.ENCODE_SEC_KEY
        self.__headers = random.choice(self.__global.HEADERS)
        self.session = requests.session()

    def __to_hex(self, encode_data):
        """16进制解码"""
        temp = 16 - len(encode_data) % 16
        return encode_data + chr(temp) * temp

    def __encode_params(self, encode_data: str = "", encode_key: str = ""):
        """解码的关键函数(1)"""
        func_iv = "0102030405060708"
        encode_data = self.__to_hex(encode_data)
        base64_sec_key = AES.new(
            key=encode_key.encode("utf-8"),
            IV=func_iv.encode("utf-8"),
            mode=AES.MODE_CBC,
        ).encrypt(encode_data.encode("utf-8"))
        return str(b64encode(base64_sec_key), "utf-8")

    def __get_params(self, encode_data: str = ""):
        """解码的关键函数(2)"""
        return self.__encode_params(
            self.__encode_params(encode_data, self.__encode_arg_g), self.__encode_arg_i
        )

    def get_response(self, url: str, encode_data: dict):
        """
        获取资源。
        需要给出 `url` 和 `encode_data` 作为参数。"""
        processed_data = {
            "params": self.__get_params(json.dumps(encode_data)),
            "encSecKey": self.__encode_sec_key,
        }
        response = self.session.post(
            url=url,
            data=processed_data,
            headers={"User-Agent": self.__headers},
            timeout=10,
        )
        return response.json()
