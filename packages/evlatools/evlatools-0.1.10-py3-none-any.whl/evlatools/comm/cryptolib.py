#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/4/30 11:18
import base64
import hashlib
from base64 import b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# AES默认的偏移量
AES_IV = "0238706044937691"

# AES默认的Key值
AES_KEY = "D4759B8149A9CF81"


class MD5(object):

    def __init__(self, text):
        self.text = text

    def encrypt(self):
        md5 = hashlib.md5()
        md5.update(self.text.encode('utf-8'))
        return md5.hexdigest()

    def decrypt(self):
        raise Exception("MD5 暂不支持解密！")


class Sha256(object):
    def __init__(self, text):
        self.text = text

    def encrypt(self):
        sha256 = hashlib.sha256()
        sha256.update(self.text.encode('utf-8'))
        return sha256.hexdigest()

    def decrypt(self):
        raise Exception("SHA256 暂不支持解密！")


class Base64(object):
    def __init__(self, text):
        self.text = text

    def encode(self):
        return base64.b64encode(self.text.encode('utf-8')).decode('utf-8')

    def decode(self):
        return base64.b64decode(self.text).decode('utf-8')


class AES(object):

    def __init__(self, text):
        self.text = text

    def encrypt(self):
        # 创建加密器实例
        cipher = Cipher(algorithms.AES(AES_KEY.encode()),
                        modes.CBC(AES_IV.encode()),
                        backend=default_backend())
        # 创建加密器
        encryptor = cipher.encryptor()

        # PKCS7填充
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(str(self.text).encode()) + padder.finalize()

        # 加密
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        # 转换为 Base64 编码
        return b64encode(encrypted).decode()


class Secret(object):

    def __init__(self, text):
        self._text = text

    def md5(self):
        return MD5(self._text)

    def sha256(self):
        return Sha256(self._text)

    def base64(self):
        return Base64(self._text)

    def aes(self):
        return AES(self._text)


def option(text, method="aes"):
    secret = Secret(text)
    method = method.lower()
    if method == "md5":
        return secret.md5()
    elif method == "sha256":
        return secret.sha256()
    elif method == "base64":
        return secret.base64()
    elif method == "aes":
        return secret.aes()
    else:
        raise ValueError(f"暂不支持的加解密方式：{method}！")


def encrypt(text, method="aes"):
    return option(text=text, method=method).encrypt()

