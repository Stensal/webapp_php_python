# -*- coding: utf-8 -*-

import os, sys
import json
import requests
import config
import logging
import libs.py6 as py6

_dir = os.path.dirname(os.path.abspath(__file__))
_appdir = os.path.abspath(os.path.join(_dir, '..'))

modpath = os.path.relpath(os.path.abspath(__file__), _appdir)
logger = logging.getLogger(modpath)


URL_AUTH = 'https://github.com/login/oauth/authorize'
URL_ACCESS_CODE = 'https://github.com/login/oauth/access_token'
URL_GET_USER = 'https://api.github.com/user'
URL_GET_REPOS = 'https://api.github.com/user/repos'


def get_authorize_url(redirect_uri, state=None):
    params = {
        'client_id': config.github['client_id'],
        'scope': 'user,repo',
        'state': state or py6.hexlify(os.urandom(8)),
        'allow_signup': 'false',
        'redirect_uri': redirect_uri
    }
    url = URL_AUTH + '?' + py6.urlencode(params)
    return url

def get_access_token(code, state=None):
    params = {
        'client_id': config.github['client_id'],
        'client_secret': config.github['client_secret'],
        'code': code,
        'state': state or py6.hexlify(os.urandom(8)),
        'allow_signup': 'false',
        'redirect_uri': ''
    }
    url = URL_ACCESS_CODE
    headers = {
        'Accept': 'application/json'
    }
    resp = requests.post(url, data=params, headers=headers)
    if resp.status_code == 200:
        d = json.loads(resp.text)
        if 'access_token' in d:
            return d

def get_user(a_token):
    params = {
        'access_token': a_token
    }
    url = URL_GET_USER + '?' + py6.urlencode(params)
    resp = requests.get(url)
    if resp.status_code == 200:
        d = json.loads(resp.text)
        return d

def get_repos(a_token, page=1, page_size=100):
    params = {
        'access_token': a_token,
        'visibility': 'all', # all|private|public
        # 'affiliation': 'owner,collaborator,organization_member',
        # 'type': 'all', # all, owner, public, private, member
        'q': '',
        'sort': 'updated',
        'direction': 'desc',
        'page': '%d' % page,
        'per_page': '%d' % page_size
    }
    url = URL_GET_REPOS + '?' + py6.urlencode(params)
    resp = requests.get(url)
    if resp.status_code == 200:
        d = json.loads(resp.text)
        return d
