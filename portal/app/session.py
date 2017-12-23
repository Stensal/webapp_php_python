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
from libs.utils import json_dumps, JSONObject
# try:
#     from Cookie import Cookie as http_cookie
# except ImportError:
#     from http.cookies import SimpleCookie as http_cookie
import flask
import config
import sqlite3
from werkzeug.local import LocalStack, LocalProxy
from functools import partial
import logging

logger = logging.getLogger('session')

COOKIE_NAME = config.cookie_name
KEY_SESSION_ID = '__session_id__'

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
        session = {}
        session[KEY_SESSION_ID] = session_id
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
        session = {}
        session[KEY_SESSION_ID] = session_id
        self.set(session_id, session)
        return session_id, session


class SessionStorageImpdByFile(object):
    
    def __init__(self, ttl=None):
        _dir = os.path.dirname(os.path.abspath(__file__))
        self.folder = os.path.join(_dir, 'sessions')
        self.folder = os.path.abspath(self.folder)

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
        session = {}
        session[KEY_SESSION_ID] = session_id
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
        session = {}
        session[KEY_SESSION_ID] = session_id
        return session_id, session

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


class Session(dict, JSONObject):

    def __init__(self, storage, session_id, session_dict):
        super(Session, self).__init__()
        self._storage = storage
        self.update(session_dict)
        self._modified = False

    def clear(self, pattern=None):
        all_keys = [k for k in self if k != KEY_SESSION_ID]
        for k in all_keys:
            del self[k]
        self._modified = True

    def save(self):
        self._storage.set(self.session_id, self)

    @property
    def session_id(self):
        return self[KEY_SESSION_ID]

    @property
    def modified(self):
        logger.debug('-- session modified? --')
        return self._modified or True

    @property
    def user(self):
        return SessionUser(self)

    def json_object(self):
        return dict(self)


class SessionInterface(flask.sessions.SessionInterface):

    def __init__(self):
        ttl = 3600 * 72 # 3 days
        self.cookie_path = '/'
        self._session_timeout = ttl
        self.storage = SessionStorage(ttl=ttl)

    def get_cookie_httponly(self, app):
        return True
    
    def get_cookie_path(self, app):
        return self.cookie_path

    def open_session(self, app, request):
        session_id = request.cookies.get(COOKIE_NAME)
        if not session_id:
            session_id, session_data = self.storage.create()
        else:
            session_data = self.storage.get(session_id)
        return Session(self.storage, session_id, session_data)

    def save_session(self, app, session, response):
        if session and KEY_SESSION_ID in session:
            session_id = session[KEY_SESSION_ID]
            self.storage.set(session_id, session)
            response.set_cookie(COOKIE_NAME, session_id, 
                                path=self.cookie_path, 
                                max_age=self._session_timeout)

class SessionUser(JSONObject):

    _keys = ('user_id',
             'unified_id', 
             'user_info',
             'privs')


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

    def json_object(self):
        user_d = None
        if self.user_info:
            user_d = dict([(k, self.user_info[k]) \
                           for k in self.user_info \
                           if k != 'github_token'])
        return {
            'user_id': self.user_id,
            'privs': self.privs,
            'user_info': user_d
        }

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
        raise AttributeError(key)
    
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

    def has_priv(self, priv):
        if not self.authenticated:
            return False
        return priv.fullfilled_by(self.privs or [])

    def save_to_session(self):
        if hasattr(self.session, 'save'):
            self.session.save()


if __name__ == '__main__':
    pass


