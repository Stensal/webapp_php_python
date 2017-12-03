#-*- coding: utf-8 -*-

import os
import re
import urllib
import functools
import flask
from flask import render_template, request, make_response
from libs.utils import json_dumps
import json
import zlib
import libs.py6 as py6
import config
import six
from session import current_user


def jview(arg):
    if isinstance(arg, str) or isinstance(arg, unicode):
        tpl_path = arg
        def wrapper_maker(view_func):
            @six.wraps(view_func)
            def wrapper(*args, **kargs):
                result = view_func(*args, **kargs)
                if isinstance(result, dict):
                    if 'user' in request.environ:
                        result['current_user'] = request.environ['user']
                    if 'debug' not in result:
                        result['debug'] = config._debug_
                    result['_r'] = py6.hexlify(os.urandom(8))
                    result['current_user'] = current_user
                    return render_template(tpl_path, **result)
                return result
            return wrapper
        return wrapper_maker
    else:
        return json_view(arg)

def json_view(arg, gzip=False):
    if isinstance(arg, dict):
        headers = arg
        def wrapper_maker(view_func):
            @six.wraps(view_func)
            def wrapper(*args, **kargs):
                _args = request.args
                callback = _args['callback'] if 'callback' in _args else None
                if request.method == 'POST':
                    _args = request.form
                    if 'callback' in _args:
                        callback = _args['callback']
                view_data = view_func(*args, **kargs)
                if isinstance(view_data, flask.Response):
                    return view_data
                if callback:
                    resp_text = json_dumps(view_data)
                    resp_text = callback+'('+resp_text+')'
                else:
                    resp_text = json_dumps(view_data)
                # -------------------- compress --------------------
                IE = re.search(r'(?:msie)|(?:boie)|(?:trident\/\d+)', 
                               request.user_agent.string, 
                               re.I|re.S)
                # print request.user_agent.string
                content_type = 'application/json;charset=UTF-8'
                compress = gzip and len(resp_text) > 1024*4
                accept_enc = request.headers['accept-encoding'] \
                    if 'accept-encoding' in request.headers else ''
                accept_enc = accept_enc or accept_enc
                accept_enc = re.split(r'[\,\;\s]+', accept_enc.lower(), re.S)
                if compress and 'deflate' in accept_enc:
                    resp = make_response(zlib.compress(resp_text))
                    # resp.content_type = 'text/javascript; charset=utf-8'
                    resp.content_type = content_type
                    if IE:
                        # IE
                        resp.headers['Content-Encoding'] = 'gzip'
                    else:
                        resp.headers['Content-Encoding'] = 'deflate'
                else:
                    resp = make_response(resp_text)
                    resp.content_type = content_type
                for h in headers:
                    resp.headers[h] = headers[h]
                return resp
            return wrapper
        return wrapper_maker
    else:
        view_func = arg
        @six.wraps(view_func)
        def wrapper(*args, **kargs):
            _resp = view_func(*args, **kargs)
            if isinstance(_resp, list) or isinstance(_resp, dict) \
                    or isinstance(_resp, tuple):
                resp = make_response(json_dumps(_resp))
                resp.content_type = 'text/javascript; charset=utf-8'
                return resp
            return _resp
        return wrapper

