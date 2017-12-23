# -*- coding: utf-8 -*-

import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))
_appdir = os.path.abspath(os.path.join(_dir, '..'))

import logging
import uuid
import json
from flask import Blueprint, request, redirect, abort
from flask import make_response, render_template
from flask import send_file, url_for
from flask import session
from ui import jview, json_view
import config
import libs.mysql_helper as my
import libs.py6 as py6
import users.github_auth as github
from libs.utils import json_dumps, _int
from users.helper import login_required, denied, user_cache
# from session import current_user
from models.helper import orm_session
from models.user import UserInfo, UserLog, GithubUser, UserPriv
import users.services
from flask import session


modpath = os.path.relpath(os.path.abspath(__file__), _appdir)
logger = logging.getLogger(modpath)

bp = Blueprint('users_bp', __name__, template_folder='templates')


@bp.route('/', methods=['POST', 'GET'])
def user_index():
    current_user = session.user
    if current_user.authenticated:
        return redirect(url_for('.github_user_welcome_page'))
    return redirect(url_for('.user_signup_choices'))

@bp.route('/welcome/', methods=['GET'])
@jview('users/welcome.html')
@login_required
def github_user_welcome_page():
    current_user = session.user
    user_info = current_user.user_info
    return {
        'title': 'Welcome',
        'user_info_json': json_dumps(user_info),
    }

@bp.route('/user/<int:user_id>/avatar.png',
          methods=['GET', 'POST'])
def user_avatar_png(user_id):
    if not user_id or user_id <= 0:
        return abort(404)
    filepath = users.services.get_user_avatar_file(user_id)
    if not filepath:
        return abort(404)
    return send_file(filepath)

@bp.route('/logout/', methods=['POST', 'GET'])
def user_logout():
    session.user.clear()
    session.save()
    return redirect(url_for('.user_index'), code=302)

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
    return redirect(fwd_url, code=302)

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
    github_user = github.get_user(a_token)
    if not github_user:
        return cb_abort(403, 'Failed to get user.')
    return _process_github_user_reg(github_user, token_d)

def _update_session_user(user_id):
    s = orm_session()
    cols = (UserInfo.user_id, \
            UserInfo.unified_id, \
            UserInfo.display_name, \
            GithubUser.github_id, \
            GithubUser.token_json, \
            GithubUser.profile_json)
    user = s.query(*cols) \
            .filter(UserInfo.user_id == user_id) \
            .one_or_none()
    if not user:
        return
    privs = s.query(UserPriv)\
             .filter(UserPriv.user_id == user_id).all()
    privs = [p.priv_code for p in privs]
    
    github_user = json.loads(user.profile_json)
    token_d = json.loads(user.token_json)
    user_d = {
        'display_name': github_user['login'],
        'github_user': github_user,
        'github_token': token_d,
    }
    session.user.user_id = user.user_id
    session.user.unified_id = user.unified_id
    session.user.user_info = user_d
    session.user.privs = privs
    session.user.save_to_session()
    return user

def _process_github_user_reg(github_user, token_d):
    if not github_user or not isinstance(github_user, dict):
        return abort(400)
    required_keys = ('id', 'html_url', 'avatar_url', 'login')
    for k in required_keys:
        if k not in github_user:
            return abort(400)
    # -- register this github user --
    sess = orm_session()
    github_id = github_user['id']
    guser = sess.query(GithubUser) \
                .filter_by(github_id=github_id).all()
    guser = guser[0] if len(guser) else None
    if not guser:
        unified_id = uuid.uuid4().hex
        luser = UserInfo(unified_id=unified_id,
                         display_name=github_user['login'])
        sess.add(luser)
        sess.commit()
        guser = GithubUser(user_id=luser.user_id)
        guser.github_id = github_user['id']
        sess.add(guser)
        # logger.debug('new user from github has been registered.')
    guser.login_name = github_user['login']
    guser.html_url = github_user['html_url']
    guser.avatar_url = github_user['avatar_url']
    guser.profile_json = json_dumps(github_user)
    guser.token_json = json_dumps(token_d)
    sess.commit()
    # logger.debug("user's profile has been updated.")

    # -------------------------------
    _update_session_user(guser.user_id)
    
    # --
    fwd_url = '/users/welcome/'
    return {
        'forward': fwd_url,
        'forward_json': json_dumps(fwd_url),
        'err': None,
        'user_id': guser.user_id
    }

@bp.route('/github/repos/', methods=['GET'])
@jview('users/github_repos.html')
@login_required
def github_get_user_repos():
    args = request.args
    if request.method == 'POST':
        args = request.form
    force_sync = _int(args.get('force_sync', '')) > 0

    user_id = session.user.user_id
    if 'github_token' not in session.user.user_info:
        return redirect(url_for('.user_logout'), code=302)
    token_d = session.user.user_info['github_token']
    a_token = token_d['access_token']
    repos = users.services.get_user_repos(user_id)
    if not repos or force_sync:
        github_repos = github.get_repos(a_token)
        repos = users.services.sync_user_repos(user_id, github_repos)
    return {
        'repos': repos,
        'repos_json': json_dumps(repos),
    }

@bp.route('/github/sync_all.<fmt>', methods=['GET', 'POST'])
@login_required
def github_sync_all(fmt):
    fmt = fmt.lower()
    if fmt not in ('json',):
        return abort(404)
    user_id = session.user.user_id
    token_d = session.user.user_info['github_token']
    a_token = token_d['access_token']
    github_repos = github.get_repos(a_token)
    repos = users.services.sync_user_repos(user_id, github_repos)
    return json_dumps({
        'repo_count': len(repos)
    })

if 'TEST_MODE' in os.environ:
    @bp.route('/create_test_session/')
    def create_test_session():
        args = request.args
        user_id = _int(args['user_id'])
        # --
        if not _update_session_user(user_id):
            return abort(403)
        # --
        resp = make_response('%d' % user_id)
        resp.status_code = 200
        resp.content_type = 'text/plain'
        return resp
        
