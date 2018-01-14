#-*- coding: utf-8 -*-

import pymysql as my
from libs.utils import namedtuple


def _utf8(obj, encoding='utf-8'):
    if isinstance(obj, str):
        return obj.decode(encoding)
    return obj

def _utf8_row(row, encoding='utf-8'):
    return [_utf8(v, encoding=encoding) for v in row]

def fetchone(cur, encoding='utf-8'):
    vals = cur.fetchone()
    if not vals:
        return
    keys = [k[0].lower() for k in cur.description]
    M = namedtuple('M', keys)
    return M(*vals)

def fetchall(cur, encoding='utf-8'):
    keys = [k[0].lower() for k in cur.description]
    M = namedtuple('M', keys)
    rows = [M(*vals) for vals in cur]
    return rows

def connect(**kargs):
    # if 'cursorclass' not in kargs:
    #     kargs['cursorclass'] = my.cursors.DictCursor
    conn = my.connect(**kargs)
    return conn


if __name__ == '__main__':
    pass

