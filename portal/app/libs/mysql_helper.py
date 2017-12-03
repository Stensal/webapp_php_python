#-*- coding: utf-8 -*-

import pymysql as my


def _utf8(obj, encoding='utf-8'):
    if isinstance(obj, str):
        return obj.decode(encoding)
    return obj

def _utf8_row(row, encoding='utf-8'):
    return [_utf8(v, encoding=encoding) for v in row]

def fetchall(cur, encoding='utf-8'):
    keys = map(lambda k: k[0].lower(), cur.description)
    rows = cur.fetchall()
    rows = map(lambda row: \
                   dict(zip(keys, _utf8_row(row, encoding=encoding))), rows)
    return rows

def connect(**kargs):
    if 'cursorclass' not in kargs:
        kargs['cursorclass'] = my.cursors.DictCursor
    conn = my.connect(**kargs)
    return conn


if __name__ == '__main__':
    pass

