# -*- coding: utf-8 -*-

import sys

PY3 = sys.version_info.major >= 3


if PY3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode

def hexlify(t):
    if PY3:
        import binascii
        return binascii.hexlify(t).decode('utf-8')
    return t.encode('hex')

