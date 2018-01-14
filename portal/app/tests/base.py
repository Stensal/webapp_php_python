# -*- coding: utf-8 -*-

import os, sys
import unittest as ut

_dir = os.path.dirname(os.path.abspath(__file__))
_rootdir = os.path.abspath(os.path.join(_dir, '../'))
if _rootdir not in sys.path:
    sys.path.append(_rootdir)

import json
from app import app
from models.helper import orm_session
from models.user import UserInfo, GithubUser
from tests.mock_data import github_token, github_get_user_resp
from tests.mock_data import github_get_repos_resp
import users.views


class TestCaseBase(ut.TestCase):

    def setUp(self):
        from models.helper import Base, engine
        Base.metadata.create_all(bind=engine, checkfirst=True)
        app.testing = True
        self.app = app
        self.client = app.test_client()
        ctx = self.app.test_request_context()
        ctx.push()

    # def tearDown(self):
    #     from models.helper import orm_session


class TestCaseBaseWithSession(TestCaseBase):

    def setUp(self):
        super(TestCaseBaseWithSession, self).setUp()
        self._create_1st_user()
        user, _ = self._create_session()
        self.user = user

    def _create_1st_user(self):
        s = orm_session()
        rs = s.query(UserInfo.user_id).first()
        s.close()
        if rs:
            return
        token_d = github_token
        github_resp = json.loads(github_get_user_resp)
        github_user = github_resp['github_user']
        rs = users.views._process_github_user_reg(github_user, token_d)

    def _create_session(self):
        github_resp = json.loads(github_get_user_resp)
        github_user = github_resp['github_user']
        s = orm_session()
        user = s.query(UserInfo.user_id) \
               .filter(UserInfo.user_id == GithubUser.user_id) \
               .filter(GithubUser.github_id == github_user['id']) \
               .one()
        s.close()

        urls = ('/users/create_test_session/', \
                '/users/create_test_session/?user_id=', \
                '/users/create_test_session/?user_id=%s' % 0,)
        for url in urls:
            resp = self.client.get(url)
            self.assertNotEqual(resp.status_code, 200)

        url = '/users/create_test_session/?user_id=%s' % user.user_id
        resp = self.client.get(url)
        return user, resp

