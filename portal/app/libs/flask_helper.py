#-*- coding: utf-8 -*-

from flask import make_response
from utils import _int
import config


def get_ip_and_ua(request_envs):
    user_agent = request_envs.get('HTTP_USER_AGENT')
    ip = request_envs.get('HTTP_X_FORWARDED_FOR')
    if not ip:
        ip = request_envs.get('REMOTE_ADDR')
    return ip, user_agent

def http_404(msg=None):
    resp = make_response(msg or u'404 not found')
    resp.status_code = 404
    return resp
