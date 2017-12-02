# -*- coding: utf-8 -*-

from flask import make_response, render_template
import six
from session import current_user


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
            if not current_user.authenticated:
                return denied(err=kargs.get('err', ''))
            return view_func(*v_args, **v_kargs)
        return wrapper
    else:
        def wrapper_maker(view_func):
            @six.wraps(view_func)
            def wrapper(*v_args, **v_kargs):
                if not current_user.authenticated:
                    return denied()
                return view_func(*v_args, **v_kargs)
            return wrapper
        return wrapper_maker

