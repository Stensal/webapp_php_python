# -*- coding: utf-8 -*-

import os, sys
import unittest as ut

_dir = os.path.dirname(os.path.abspath(__file__))
_rootdir = os.path.abspath(os.path.join(_dir, '../'))
if _rootdir not in sys.path:
    sys.path.append(_rootdir)

import logging
from tests.base import TestCaseBase
from tests.test_user import UserTest


class AppTest(TestCaseBase):

    def test_front_pages(self):
        resp = self.client.get('/', follow_redirects=True)
        self.assertTrue(resp.status_code == 200)
        resp = self.client.get('/products/')
        self.assertTrue(resp.status_code == 200)
        resp = self.client.get('/demo/')
        self.assertTrue(resp.status_code == 200)
        resp = self.client.get('/issues/')
        self.assertTrue(resp.status_code == 200)
        resp = self.client.get('/users/signup/')
        self.assertTrue(resp.status_code == 200)



if __name__ == '__main__':
    os.environ['TEST_MODE'] = 'On'
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger('tests').setLevel(logging.DEBUG)
    t_all = ut.TestSuite()
    t_all.addTest(AppTest())
    t_all.addTest(UserTest())
    ut.main(verbosity=2, argv=sys.argv[:1])

