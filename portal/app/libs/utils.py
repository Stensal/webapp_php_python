#-*- coding: utf-8 -*-

import os
import re
import logging
import datetime, time
import random
import math
import json
from decimal import Decimal
import functools
import six
# from sqlalchemy.ext.declarative import DeclarativeMeta

logger = logging.getLogger(__name__)


class NTuple(object):

    def __init__(self, meta, *vals):
        self.meta = meta
        self.vals = vals if isinstance(vals, list) else list(vals)

    def __dir__(self):
        return self.meta.keys

    def __contains__(self, key):
        return key in self.meta.keys

    def __getitem__(self, key):
        return self.vals[self.meta.idx[key]]

    def __setitem__(self, key, value):
        if key not in self.meta.idx:
            self.meta.add_key(key)
        i = self.meta.idx[key]
        if i >= len(self.vals):
            self.vals.append(value)
        else:
            self.vals[i] = value

    def __getattr__(self, key):
        if key in self.meta.keys:
            return self.vals[self.meta.idx[key]]
        raise AttributeError(key)

    # def __setattr__(self, key, value):
    #     if key in self.meta.keys:
    #         self.vals[self.meta.idx[key]] = value
    #     else:
    #         super(NTuple, self).__setattr__(key, value)

    def _asdict(self):
        return dict([(k, self.vals[self.meta.idx[k]]) \
                     for k in self.meta.idx])


class NTupleMeta(object):

    def __init__(self, _, keys):
        self.keys = keys
        self.idx = dict([(k, i) for i, k in enumerate(keys)])

    def add_key(self, key):
        if key not in self.idx:
            self.keys.append(key)
            self.idx[key] = len(self.keys) - 1

    def __call__(self, *vals):
        return NTuple(self, *vals)


def namedtuple(name, keys):
    return NTupleMeta(name, keys)


class CommonJSONEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if six.PY3:
            if isinstance(obj, bytes):
                return obj.decode('utf-8')
        else:
            if isinstance(obj, str):
                return obj.decode('utf-8')
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, NTuple):
            return obj._asdict()
        if isinstance(obj, JSONObject):
            return obj.json_object();
        if hasattr(obj, '__json__'):
            return obj.__json__()
        return json.JSONEncoder.default(self, obj);
        # return super(CommonJSONEncoder, self).default(obj)


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

def _date_iso8601(t):
    if not t or not isinstance(t, (str, bytes)):
        raise ValueError('a str argument required.')
    if isinstance(t, bytes):
        t = t.decode('utf-8')
    fmt = '%Y-%m-%dT%H:%M:%SZ'
    d = datetime.datetime.strptime(t, fmt)
    return d
