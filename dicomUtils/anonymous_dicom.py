# -*- coding: utf-8 -*-

"""
@author yaoxs@democompany.net
@date 2019/11/21 11:11
"""
# -*- coding: utf-8 -*-
import os
import base64
from Crypto.Cipher import AES


class AnonymousDicom:
    """
    脱敏加密解密逻辑
    """
    def __init__(self):
        self._block_size = AES.block_size
        self._key = self._add_to_32('JdOi4TMm!D')
        self._iv = bytes.fromhex('f423e7f12d37be4137a95fea20015437')
        self.aes = AES.new(self._key, AES.MODE_CBC, self._iv)

    @staticmethod
    def _add_to_32(s):
        """
        补足字符串长度为32的倍数
        :param s:
        :return:
        """
        while len(s) % 32 != 0:
            s += '\0'
        return str.encode(s)  # 返回bytes

    def encrypt(self, text: str):
        """
        加密
        :param text:
        :return:
        """
        encrypt_byte = self.aes.encrypt(str.encode(self._pad(text)))
        base64_encrpyt_str = base64.encodebytes(self._iv + encrypt_byte)
        return str(base64_encrpyt_str, encoding='utf8').replace('\n', '')

    def _pad(self, text):
        return text + (self._block_size - len(text) % self._block_size) * \
               chr(self._block_size - len(text) % self._block_size)

    def decrypt(self, text: str):
        """
        解密
        :param text:
        :return:
        """
        text = base64.b64decode(text)
        decrypt_content = self.aes.decrypt(text[self._block_size:])
        return str(self._unpad(decrypt_content).decode("utf8"))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


anonymous_dicom = AnonymousDicom()
# wait_ecrpyt = 'Anonymous'
# print(anonymous_dicom.encrypt(wait_ecrpyt))
content = anonymous_dicom.decrypt('9CPn8S03vkE3qV/qIAFUN+ABuRswaGeK+1i1QZvNBsA=')
print(content)
