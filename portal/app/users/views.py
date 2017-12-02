# -*- coding: utf-8 -*-

import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))
_appdir = os.path.abspath(os.path.join(_dir, '..'))

import logging
from flask import Blueprint, request, redirect, abort
from flask import make_response, render_template
from flask import send_file
from ui import jview, json_view
import config
import libs.mysql_helper as my
import libs.py6 as py6
import users.github_auth as github
from libs.utils import json_dumps
from users.helper import login_required, denied
from session import session, current_user


modpath = os.path.relpath(os.path.abspath(__file__), _appdir)
logger = logging.getLogger(modpath)

bp = Blueprint('users_bp', __name__, template_folder='templates')


@bp.route('/', methods=['POST', 'GET'])
def user_index():
    if current_user.authenticated:
        return redirect('/users/welcome/')
    return redirect('/users/signup/')

@bp.route('/welcome/', methods=['GET'])
@jview('users/welcome.html')
@login_required
def github_user_welcome_page():
    user_info = current_user.user_info
    return {
        'title': 'Welcome',
        'user_info_json': json_dumps(user_info),
    }

@bp.route('/logout/', methods=['POST', 'GET'])
def user_logout():
    session.clear()
    session.save()
    return redirect('/')

@bp.route('/signup/', methods=['POST', 'GET'])
@jview('users/signup.html')
def user_signup_choices():
    return {'title': 'Signup'}

@bp.route('/github/oauth_start/', methods=['GET'])
def github_oauth_start():
    args = request.args
    if request.method == 'POST':
        args = request.form
    serv_prefix = args.get('serv_prefix', '')
    if not serv_prefix:
        return abort(400)
    redirect_uri = serv_prefix
    while redirect_uri.endswith('/'):
        redirect_uri = redirect_uri[:-1]
    redirect_uri += '/users/github/oauth_callback/'
    state = py6.hexlify(os.urandom(8))
    session['github_oauth_state'] = state
    session.save()
    fwd_url = github.get_authorize_url(redirect_uri, state=state)
    return redirect(fwd_url)

def cb_abort(code, text):
    vdata = {
        'err': '%s %s' % (code, text),
        'forward': None,
        'forward_json': '"#"',
    }
    t = render_template('users/github_callback.html', **vdata)
    resp = make_response(t)
    resp.status_code = code
    return resp

@bp.route('/github/oauth_callback/', methods=['GET'])
@jview('users/github_callback.html')
def github_oauth_callback():
    args = request.args
    if request.method == 'POST':
        args = request.form
    code = args.get('code', '')
    state = args.get('state', '')
    if not state or not code:
        return cb_abort(400, 'Bad request.')
    if state != session['github_oauth_state']:
        return cb_abort(403, 'Invalid state.')
    token_d = github.get_access_token(code)
    if not token_d:
        return cb_abort(403, 'Failed to obtain access token.')
    session['github_access_token'] = token_d
    session.save()
    a_token = token_d['access_token']
    # -- get user
    user_info = current_user.user_info
    github_user = github.get_user(a_token)
    if not github_user:
        return cb_abort(403, 'Failed to get user.')
    user_d = {
        'github_user': github_user
    }
    current_user.unified_id = py6.hexlify(os.urandom(8))
    current_user.user_info = user_d
    current_user.save_to_session()
    # --
    fwd_url = '/users/welcome/'
    return {
        'forward': fwd_url,
        'forward_json': json_dumps(fwd_url),
        'err': None,
    }

@bp.route('/github/repos/', methods=['GET'])
@jview('users/github_repos.html')
@login_required
def github_get_user_repos():
    token_d = session['github_access_token']
    if not token_d:
        return denied('You should signin with github first.')
    a_token = token_d['access_token']
    if not a_token:
        return denied(err='Invalid access token.')
    repos = github.get_repos(a_token)
    return {
        'repos': repos,
        'repos_json': json_dumps(repos),
    }

