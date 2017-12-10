#-*- coding: utf-8 -*-

import os, sys

_dir = os.path.dirname(os.path.abspath(__file__))

import time
import base64
import json
import re
import hashlib
import random
import redis
import datetime
import uuid
from libs.utils import json_dumps
try:
    from Cookie import Cookie as http_cookie
except ImportError:
    from http.cookies import SimpleCookie as http_cookie
import flask
import config
import sqlite3
from werkzeug.local import LocalStack, LocalProxy
from functools import partial
import logging


COOKIE_NAME = config.cookie_name

def _create_redis_pool():
    if 'redis' not in config.session_storage:
        return
    if 'unix_socket' in config.session_storage['redis']:
        _path = config.session_storage['redis']['unix_socket']
        return redis.ConnectionPool(
            connection_class=redis.UnixDomainSocketConnection,
            path=_path)
    else:
        _host = config.session_storage['redis']['host']
        _port = config.session_storage['redis']['port']
        _db = config.session_storage['redis']['db']
        return redis.ConnectionPool(host=_host, port=_port, db=_db)

class SessionStorageImpdByRedis(object):

    pool = _create_redis_pool()

    def __init__(self, ttl=None):
        self.pool = self.__class__.pool
        self.conn = redis.Redis(connection_pool=self.pool)
        self.TTL = ttl or 3600 * 24 * 3 # 3 days

    def clear(self, session_id):
        self.conn.expire(session_id, 0)

    def get(self, session_id):
        if not session_id:
            return
        data = self.conn.get(session_id)
        if data:
            return json.loads(data)

    def set(self, session_id, session_dict):
        if not session_id:
            return
        if not session_dict:
            self.clear(session_id)
        data = json_dumps(session_dict)
        self.conn.set(session_id, data)
        self.conn.expire(session_id, self.TTL)

    def extend_session_ttl(self, session_id, seconds):
        ttl = self.conn.ttl(session_id)
        ttl = ttl or 0
        if ttl <= seconds:
            self.conn.expire(session_id, seconds)

    def create(self):
        rnd_str = base64.b64encode(os.urandom(128))
        session_id = hashlib.sha1(rnd_str).hexdigest()
        # now = datetime.datetime.now()
        # session_id = '%s-%s' % (now.strftime('%Y%m%d%H%M%S'), session_id)
        session = {
            '__session_id__': session_id
            }
        self.set(session_id, session)
        return session_id, session


class SessionStorageImpdBySqlite(object):

    data_dir = os.path.join(_dir, 'sessions')
    data_path = os.path.join(data_dir, 'sessions.db')

    def __init__(self, ttl=None):
        cls = self.__class__
        self.TTL = ttl or 3600 * 24 * 3 # 3 days
        if not os.path.isdir(cls.data_dir):
            os.makedirs(cls.data_dir)
        if not os.path.isfile(cls.data_path):
            # self._init_db()
            pass

    def _conn(self):
        cls = self.__class__
        conn = None
        conn = sqlite3.connect(cls.data_path)
        cur = conn.cursor()
        sql = ("select 1 from sqlite_master ",
               " where type='table' and name=? ")
        cur.execute(''.join(sql), ('t_session', ))
        if not cur.fetchone():
            sql = ('create table t_session ',
                   '( session_id text primary key, ',
                   '  session_data text, ',
                   '  last_update integer ) ',)
            cur.execute(''.join(sql))
        cur.close()
        return conn

    def clear(self, session_id):
        conn, cur = None, None
        try:
            conn = self._conn()
            cur = conn.cursor()
            sql = 'delete from t_session where session_id=?'
            cur.execute(sql, (session_id,))
            conn.commit()
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get(self, session_id):
        if not session_id:
            return
        conn, cur = None, None
        try:
            conn = self._conn()
            cur = conn.cursor()
            sql = ('select session_data ',
                   '  from t_session ',
                   ' where session_id=? ',
                   '   and last_update>=? ',)
            t = int(time.time() - self.TTL)
            cur.execute(''.join(sql), (session_id, t, ))
            row = cur.fetchone()
            if row:
                data = row[0]
                if data:
                    return json.loads(data)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def set(self, session_id, session_dict):
        if not session_id:
            return
        if not session_dict:
            self.clear(session_id)
        data = json_dumps(session_dict)
        conn, cur = None, None
        try:
            conn = self._conn()
            cur = conn.cursor()
            sql = 'select 1 from t_session where session_id=?'
            cur.execute(sql, (session_id,))
            row = cur.fetchone()
            t = int(time.time())
            if row:
                sql = ('update t_session ',
                       '   set session_data=?, last_update=? ',
                       ' where session_id=?')
                cur.execute(''.join(sql), (data, t, session_id,))
            else:
                sql = ('insert into t_session ',
                       ' (session_id, session_data, last_update) ',
                       ' values ',
                       ' (?, ?, ?) ',)
                cur.execute(''.join(sql), (session_id, data, t))
            conn.commit()
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def extend_session_ttl(self, session_id, seconds):

        conn, cur = None, None
        try:
            conn = self._conn()
            cur = conn.cursor()
            t = int(time.time())
            sql = ('update t_session ',
                   '   set last_update=? ',
                   ' where session_id=?')
            cur.execute(''.join(sql), (t, session_id,))
            conn.commit()
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def create(self):
        session_id = uuid.uuid1().hex
        session = {
            '__session_id__': session_id
            }
        self.set(session_id, session)
        return session_id, session


class SessionStorageImpdByFile(object):
    
    def __init__(self, ttl=None):
        _dir = os.path.dirname(os.path.abspath(__file__))
        self.folder = os.path.join(_dir, 'sessions')
        self.folder = os.path.abspath(self.folder)
        # app_startup_dir = os.environ['-wsgi-startup-dir']
        # self.folder = os.path.join(app_startup_dir, './sessions')
        # self.folder = os.path.abspath(self.folder)

    def _check_folder(self):
        if not os.access(self.folder, os.F_OK):
            os.makedirs(self.folder)

    def clear(self, session_id):
        assert session_id
        self._check_folder()
        data_path = os.path.join(self.folder, session_id)
        if os.access(data_path, os.F_OK):
            os.unlink(data_path)

    def get(self, session_id):
        assert session_id
        session = {
            '__session_id__': session_id
            }
        self._check_folder()
        data_path = os.path.join(self.folder, session_id)
        if os.access(data_path, os.F_OK):
            with open(data_path, 'rb') as f:
                _session_str = f.read()
                if _session_str:
                    session.update(json.loads(_session_str))
                f.close()
        return session

    def set(self, session_id, session_dict):
        assert len(session_id)>0
        self._check_folder()
        data_path = os.path.join(self.folder, session_id)
        if len(session_dict) >= 1:
            with open(data_path, 'wb+') as f:
                f.write(json_dumps(session_dict).encode('utf-8'))
                f.close()
        else:
            if os.access(data_path, os.F_OK):
                os.unlink(data_path)

    def extend_session_ttl(self, session_id, seconds):
        pass

    def create(self):
        rnd_str = None
        session_id = None
        while True:
            rnd_str = base64.b64encode(os.urandom(128))
            session_id = hashlib.sha1(rnd_str).hexdigest()[:16]
            if not os.access(os.path.join(self.folder, session_id), 
                             os.F_OK):
                break
        return session_id, {
            '__session_id__': session_id
            }

#class SessionStorage(SessionStorageImpdByRedis): pass
#class SessionStorage(SessionStorageImpdByFile): pass

# if config._debug_:
#     class SessionStorage(SessionStorageImpdBySqlite): pass
# else:
#     class SessionStorage(SessionStorageImpdByRedis): pass

    
if 'redis' in config.session_storage:
    SessionStorage = SessionStorageImpdByRedis
else:
    SessionStorage = SessionStorageImpdByFile


class StandaloneSession(object):

    def __init__(self, session_id, ttl=None):
        self.session_id = session_id
        self.storage = SessionStorage(ttl=ttl)
        self.session = None
        if self.session_id:
            self.session = self.storage.get(self.session_id)
        if not self.session:
            self.session_id, self.session = self.storage.create()

    def has_key(self, key):
        return self.session.has_key(key)

    def __getitem__(self, key):
        return self.session[key] if key in self.session else None

    def __setitem__(self, key, val):
        self.session[key] = val

    def __contains__(self, key):
        return key in self.session

    def __iter__(self):
        for k in self.session:
            yield k

    def __delitem__(self, key):
        if key in self.session:
            del self.session[key]

    def extend_ttl(self, seconds):
        self.storage.extend_session_ttl(self.session_id, seconds)

    def save(self):
        self.storage.set(self.session_id, self.session)

    def clear(self):
        # self.storage.clear(self.session_id)
        self.session = {
            '__session_id__': self.session_id
        }


def get_session(session_id, ttl=None):
    return StandaloneSession(session_id, ttl=ttl)

class SessionInterface(flask.sessions.SessionInterface):

    def __init__(self):
        ttl = 3600 * 72 # 3 days
        self.cookie_path = '/'
        self._session_timeout = ttl
        self.storage = SessionStorage(ttl=ttl)
    
    def get_cookie_path(self, app):
        return self.cookie_path

    def open_session(self, app, request):
        session_id = request.cookies.get(COOKIE_NAME)
        if not session_id:
            session_id, session = self.storage.create()
            return session
        else:
            return self.storage.get(session_id)

    def save_session(self, app, session, response):
        if session and session.has_key('__session_id__'):
            session_id = session['__session_id__']
            assert len(session_id)>0
            self.storage.set(session_id, session)
            response.set_cookie(COOKIE_NAME, session_id, 
                                path=self.cookie_path, 
                                max_age=self._session_timeout)


class SessionUser(object):

    _keys = ('user_id',
             'unified_id', 
             'user_info',)


    def __str__(self):
        return '<SessionUser ' \
            + ('authorized' if self.authenticated else 'unauthorized') \
            + ', ' + self.user_label \
            + '>'

    def __init__(self, session):
        self.session = session

    @property
    def session_id(self):
        return self.session.session_id

    def get_dict(self):
        return dict([(k, self[k]) for k in self.__class__._keys])

    def get_value(self, key):
        if key in self.__class__._keys:
            _key = 'user:%s' % key
            if _key in self.session:
                return self.session[_key]
            return None

    def set_value(self, key, value):
        if key in self.__class__._keys:
            _key = 'user:%s' % key
            self.session[_key] = value

    def __getattr__(self, key):
        if key in self.__class__._keys:
            return self.get_value(key)
        return super(SessionUser, self).__getattr__(key)
    
    def __setattr__(self, key, value):
        if key in self.__class__._keys:
            self.set_value(key, value)
        super(SessionUser, self).__setattr__(key, value)

    def __getitem__(self, key):
        return self.get_value(key)

    def __setitem__(self, key, value):
        self.set_value(key, value)

    def __contains__(self, key):
        return key in self.__class__._keys and key in self.session

    def clear(self):
        self.session.clear()
        self.session.save()

    @property
    def user_label(self):
        if self.authenticated:
            label = self.user_info.get('display_name', '')
        return label or '$SessionUser.noname'

    @property
    def authenticated(self):
        if self.user_id and self.user_info:
            return True
        return False

    def save_to_session(self):
        if hasattr(self.session, 'save'):
            self.session.save()

_session_stack = LocalStack()

def _get_attr_of_top(name):
    top = _session_stack.top
    if not top:
        return None
    return getattr(top, name)

session = LocalProxy(partial(_get_attr_of_top, '_session'))
current_user = LocalProxy(partial(_get_attr_of_top, '_user'))

class SessionMiddleware(object):
    
    def __init__(self, app):
        self.app = app
        self._session = None
        self._user = None

    def __call__(self, *args):
        try:
            _session_stack.push(self)
            return self._call(*args)
        finally:
            _session_stack.pop()

    def _call(self, environ, start_response):
        # ---- no cookies for static contents ----
        request_path = environ['PATH_INFO']
        l_path = request_path.lower()
        is_static = l_path.startswith('/static/')
        is_static = is_static or l_path.startswith('/v/')
        if is_static:
            return self.app(environ, start_response)
        # ----
        ua = None
        if 'HTTP_USER_AGENT' in environ:
            ua = environ['HTTP_USER_AGENT']
        ua = ua or ''
        is_mobi = re.search(r'iphone|android', ua, re.I|re.S)
        cookies = http_cookie()
        raw_req_cookies = ''
        if 'HTTP_COOKIE' in environ:
            raw_req_cookies = environ['HTTP_COOKIE']
        try:
            cookies.load(raw_req_cookies)
        except Exception as e:
            logging.error(traceback.format_exc(e))
            # print >> sys.stderr, '-'*40
            # print >> sys.stderr, 'cookies load error.'
            # print >> sys.stderr, e.message
            # print e.message
            raise
        flush_rssid = False # should overwrite rss-id
        # flush_rssut = False # should overwrite rss-update-time
        ttl = 3600 * 24 * 3
        ttl_step = 60 * 30
        if is_mobi:
            ttl = 3600 * 24 * 15
            ttl_step = 3600 * 24 * 7
        if COOKIE_NAME in cookies: #cookies.has_key(COOKIE_NAME):
            session_id = cookies[COOKIE_NAME].coded_value
            session = get_session(session_id, ttl=ttl)
            if session_id != session.session_id:
                session_id = session.session_id
                flush_rssid = True
            environ['session'] = session
        else:
            session = get_session(None, ttl=ttl)
            session_id = session.session_id
            environ['session'] = session
            flush_rssid = True
        # extend the ttl of session
        session.extend_ttl(ttl_step)
        self._session = session
        self._user = SessionUser(session)
        environ['user'] = self._user
        def _start_response(status, headers, exc_info=None):
            if flush_rssid:
                max_age = int(ttl * 1.5)
                rssid_str = '%s=%s; path=/; max-age=%d; httponly' % (
                    COOKIE_NAME, session_id, max_age)
                headers.append(('set-cookie', rssid_str))
            return start_response(status, headers)
        return self.app(environ, _start_response)


if __name__ == '__main__':
    pass


