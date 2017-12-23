# -*- coding: utf-8 -*-

import logging
import urllib.parse
import json
from tests.base import TestCaseBaseWithSession
from models.user import UserInfo, GithubUser
from models.helper import orm_session
from tests.mock_data import github_token, github_get_user_resp
from tests.mock_data import github_get_repos_resp
import users.views
import users.services


logger = logging.getLogger('tests')


class UserTest(TestCaseBaseWithSession):

    def setUp(self):
        super(UserTest, self).setUp()

    def test_user_query(self):
        s = orm_session()
        self.assertIsNotNone(s.query(UserInfo).all()[:10])
        s.close()

    def test_user_avatar(self):
        s = orm_session()
        rs = s.query(GithubUser).first()
        if rs:
            user_id = rs.user_id
            # fname = users.services.get_user_avatar_file(user_id)
            url = '/users/user/%s/avatar.png' % user_id
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
        s.close()

    def test_github_oauth2(self):
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

    def test_github_user_register(self):
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
        s.close()
        self.assertIsNotNone(user)
        self.assertEqual(user.github_id, github_user['id'])

    def test_list_repos(self):
        resp = self.client.get('/users/github/repos/')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/users/github/repos/?force_sync=1')
        self.assertEqual(resp.status_code, 200)

    def test_sync_repos(self):
        user = self.user
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

        rs = json.loads(resp.data)
        self.assertIsNotNone(rs)
        self.assertTrue(isinstance(rs, dict))



class UserLogoutTest(TestCaseBaseWithSession):

    def setUp(self):
        super(UserTest, self).setUp()

    def _logout(self):
        url = '/users/logout/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(url, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

    def tearDown(self):
        self._logout()
        super(UserTest, self).tearDown()

