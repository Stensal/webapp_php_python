#-*- coding: utf-8 -*-

import os
import re
import datetime
import random
import math
import json
from decimal import Decimal
import functools

class CommonJSONEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, JSONObject):
            return obj.json_object();
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj);


class JSONObject(object):
    
    def json_object(self):
        raise NotImplementedError('json_object')


def json_dumps(objects):
    return json.dumps(objects, cls=CommonJSONEncoder)

def is_nan(a):
    return (isinstance(a, float) and math.isnan(a)) or a!=a

def _float(text):
    if not text:
        return 0.0
    if isinstance(text, Decimal):
        return float(text)
    if isinstance(text, float) or isinstance(text, int):
        return text
    if re.match(r'^(?:[-+])?\d+(?:\.\d+)?$', text):
        return float(text)
    return 0.0

def _int(text):
    if not text:
        return 0
    if isinstance(text, Decimal):
        return int(text)
    if isinstance(text, int):
        return text
    if re.match(r'^(?:[-+])?\d+$', text):
        return int(text)
    return 0

def _date(text):
    pt_date_1 = r'^(?P<y>\d{4})(?P<mon>\d{2})(?P<d>\d{2})'
    pt_date_2 = r'^(?P<y>\d{4})[./-](?P<mon>\d{1,2})[./-](?P<d>\d{1,2})'
    pt_time = r'(?P<hh>\d+)\:(?P<mm>\d+)\:(?P<ss>\d+)'
    pts = (pt_date_2 + r'\s+' + pt_time,
           pt_date_2,
           pt_date_1,
           )
    for pt in pts:
        m = re.search(pt, text, re.I|re.S)
        if m:
            _m = m.groupdict()
            if 'y' in _m:
                y = int(_m['y'])
                mon = int(_m['mon'])
                d = int(_m['d'])
                if 'hh' in _m:
                    hh = int(_m['hh'])
                    mm = int(_m['mm'])
                    ss = int(_m['ss'])
                    return datetime.datetime(y, mon, d, hh, mm, ss)
                else:
                    return datetime.datetime(y, mon, d, 0, 0, 0)
    pt_yyyymm = r'^(?P<y>\d{4})(?P<mon>\d{2})$'
    m = re.search(pt_yyyymm, text, re.I|re.S)
    if m:
        _m = m.groupdict()
        y, mon = int(_m['y']), int(_m['mon'])
        return datetime.datetime(y, mon, 1, 0, 0, 0)

