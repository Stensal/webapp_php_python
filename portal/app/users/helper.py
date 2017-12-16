# -*- coding: utf-8 -*-

import json
import hashlib
from flask import make_response, render_template, session
import redis
import six
from libs.utils import json_dumps
import config


def denied(err=None):
    tpl = 'users/login_required.html'
    vdata = {'err': err or 'Access denied.'}
    resp = make_response(render_template(tpl, **vdata))
    resp.content_type = 'text/html'
    return resp

def login_required(*args, **kargs):
    if len(args) == 1 and callable(args[0]) and not kargs:
        view_func = args[0]
        @six.wraps(view_func)
        def wrapper(*v_args, **v_kargs):
            current_user = session.user
            if not current_user.authenticated:
                return denied(err=kargs.get('err', ''))
            return view_func(*v_args, **v_kargs)
        return wrapper
    else:
        def wrapper_maker(view_func):
            @six.wraps(view_func)
            def wrapper(*v_args, **v_kargs):
                current_user = session.user
                if not current_user.authenticated:
                    return denied()
                return view_func(*v_args, **v_kargs)
            return wrapper
        return wrapper_maker

def user_cache(cache_key, ttl=3600):
    def wrapper_maker(view_func):
        @six.wraps(view_func)
        def wrapper(*v_args, **v_kargs):
            _key = None
            if cache_key:
                key0 = hashlib.md5(json_dumps(args)).hexdigest()
                key1 = hashlib.md5(json_dumps(kargs)).hexdigest()
                current_user = session.user
                uid = current_user.unified_id or '-'
                _key = '%s-%s:%s-%s' % (uid, cache_key, key0, key1)
                found, data = cache_fetch(_key)
                if found:
                    return data
            data = view_func(*v_args, **v_kargs)
            if _key:
                cache_store(_key, data, ttl)
            return data
        return wrapper
    return wrapper_maker

def cache_fetch(cache_key):
    '''returns a tuple (found, data)'''
    if not cache_key:
        return
    url = 'redis://%(host)s:6379/%(db)s' % config.cache['redis']
    t = r.get(cache_key)
    if t:
        return True, json.loads(t)
    return False, None

def cache_store(cache_key, data, ttl):
    if not cache_key:
        return
    if ttl < 0:
        ttl = 0
    t = json_dumps(data)
    url = 'redis://%(host)s:6379/%(db)s' % config.cache['redis']
    r = redis.from_url(url)
    r.set(cache_key, t)
    r.expire(cache_key, ttl)

def clear_cache(cache_key):
    if not cache_key:
        return
    url = 'redis://%(host)s:6379/%(db)s' % config.cache['redis']
    r = redis.from_url(url)
    r.expire(cache_key, 0)

