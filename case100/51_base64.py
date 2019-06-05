# -*- coding: UTF-8 -*-
# base64 是一种用64个字符来表示任意二进制数据的方法

import base64

print(base64.b64encode(b'binary'))
print(base64.b64decode(b'YmluYXJ5'))


def safe_base64_decode(s):
    return base64.b64decode(s + ((len(s) % 4) * b'='))


def safe_base64_decode2(s):
    return s.rstrip('=')


print(safe_base64_decode(b'YWJjZA=='))
print(safe_base64_decode('YWJjZA=='))
