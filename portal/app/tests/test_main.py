# -*- coding: utf-8 -*-

import os, sys
import unittest as ut

_dir = os.path.dirname(os.path.abspath(__file__))
_rootdir = os.path.abspath(os.path.join(_dir, '../'))
if _rootdir not in sys.path:
    sys.path.append(_rootdir)

os.environ['TEST_MODE'] = 'On'

import logging

logfmt = '[%(levelname)-5s] %(name)6s: %(message)s'
logging.basicConfig(stream=sys.stdout, 
                    level=logging.DEBUG,
                    format=logfmt)
logging.getLogger('tests').setLevel(logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.INFO)
logging.getLogger('sqlalchemy').setLevel(logging.WARNING)

from tests.base import TestCaseBase
from tests.test_user import UserTest, UserLogoutTest
from tests.test_utils import UtilsTest
from tests.test_issue import IssueTest


class AppTest(TestCaseBase):

    def test_front_pages(self):
        resp = self.client.get('/', follow_redirects=True)
        self.assertTrue(resp.status_code == 200)
        resp = self.client.get('/products/')
        self.assertTrue(resp.status_code == 200)
        resp = self.client.get('/demo/')
        self.assertTrue(resp.status_code == 200)
        resp = self.client.get('/issues/')
        self.assertTrue(resp.status_code in (200, 301, 302))
        resp = self.client.get('/users/signup/')
        self.assertTrue(resp.status_code == 200)



if __name__ == '__main__':
    t_all = ut.TestSuite()
    t_all.addTest(AppTest())
    t_all.addTest(UserTest())
    t_all.addTest(UserLogoutTest())
    t_all.addTest(UtilsTest())
    t_all.addTest(IssueTest())
    ut.main(verbosity=2, argv=sys.argv[:1])

