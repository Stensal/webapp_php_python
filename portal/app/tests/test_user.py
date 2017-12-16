# -*- coding: utf-8 -*-

import logging
import urllib.parse
import json
from tests.base import TestCaseBase
from models.user import UserInfo, GithubUser
from models.helper import orm_session
from tests.mock_data import github_token, github_get_user_resp
from tests.mock_data import github_get_repos_resp
import users.views
import users.services


logger = logging.getLogger('tests')


class UserTest(TestCaseBase):

    def test_user_query(self):
        s = orm_session()
        self.assertIsNotNone(s.query(UserInfo).all())
        s.close()

    def test_github_start(self):
        '''perform a redirect to github oauth2.'''
        prefix = urllib.parse.quote('http://localhost')
        path1 = '/users/github/oauth_start'
        path2 = path1 + '?serv_prefix='
        path3 = path2 + prefix
        # resp = self.client.get(path1, follow_redirects=False)
        # self.assertTrue(resp.status_code not in (301, 302),
        #                 msg='status_code: %s' % resp.status_code)
        # resp = self.client.get(path2, follow_redirects=False)
        # self.assertTrue(resp.status_code in (301, 302),
        #                 msg='status_code: %s' % resp.status_code)
        resp = self.client.get(path3, follow_redirects=False)
        self.assertTrue(resp.status_code in (301, 302),
                        msg='status_code: %s' % resp.status_code)

    def test_create_github_user(self):
        '''register a github user and find it in db.'''
        token_d = github_token
        github_resp = json.loads(github_get_user_resp)
        github_user = github_resp['github_user']
        with self.app.test_request_context():
            rs = users.views._process_github_user_reg(github_user, token_d)
            self.assertIsNotNone(rs)
            self.assertTrue('user_id' in rs)
            self.assertGreater(rs['user_id'], 0)
            user_id = rs['user_id']

        s = orm_session()
        user = s.query(UserInfo.user_id, GithubUser.github_id) \
                .filter(UserInfo.user_id==GithubUser.user_id) \
                .filter(GithubUser.user_id==user_id) \
                .one()
        self.assertIsNotNone(user)
        self.assertEqual(user.github_id, github_user['id'])

    def test_repos(self):
        '''diff repos between local's and github's.'''
        github_resp = json.loads(github_get_user_resp)
        github_user = github_resp['github_user']
        s = orm_session()
        user = s.query(UserInfo.user_id) \
               .filter(UserInfo.user_id == GithubUser.user_id) \
               .filter(GithubUser.github_id == github_user['id']) \
               .one()
        repos = json.loads(github_get_repos_resp)
        rs = users.services.sync_user_repos(user.user_id, repos)
        self.assertIsNotNone(rs)
        self.assertTrue(rs)

    def test_sync_all(self):
        resp = self.client.get('/users/github/sync_all.json')
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.data)
        self.assertTrue(isinstance(resp.data, (str, bytes)))
        self.assertGreater(len(resp.data), 0)
        logger.debug(resp.data)
        rs = json.loads(resp.data)
        self.assertIsNotNone(rs)
        self.assertEqual(isinstance(rs, dict))

