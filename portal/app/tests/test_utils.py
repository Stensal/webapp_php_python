# -*- coding: utf-8 -*-

import os, sys

_dir = os.path.dirname(os.path.abspath(__file__))
_rootdir = os.path.abspath(os.path.join(_dir, '../'))
if _rootdir not in sys.path:
    sys.path.append(_rootdir)

import datetime, time
import logging
import json
from libs.utils import namedtuple
import unittest as ut
from libs.utils import _date_iso8601, _date, json_dumps
from models.repo import Repo


logger = logging.getLogger('tests')


class UtilsTest(ut.TestCase):

    def test_date_process(self):
        texts = ('', \
                 None, \
                 2245, \
                 os.urandom(32), \
                 '2017/02', \
                 '2017-07-21', \
                 '2017-12-04 22:03', \
                 '2017-12-04 22:03:17',)
        for t in texts:
            self.assertRaises(ValueError, _date_iso8601, t)
        t = '2017-12-04T22:03:17Z'
        d = _date_iso8601(t)
        self.assertIsNotNone(d)
        self.assertEqual(int(d.timestamp()), 1512424997)

    def test_json_dumps(self):
        M = namedtuple('M', ('x', 'y', 'name'))
        m0 = M(1, 2, 'central')
        objs = (123, \
                True, \
                None, \
                {'x': 123}, \
                [1, 2, 3], \
                ('a', 'b', 'c'), \
                {'x': [1,2,3]}, \
                Repo(repo_id=123, repo_name='cpp'), \
                datetime.datetime.now(), \
                time.time(), \
                '汉字', \
                m0, )
        for obj in objs:
            self.assertTrue(isinstance(json_dumps(obj), str))
        m1 = json.loads(json_dumps(m0))
        self.assertTrue(isinstance(m1, dict))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    ut.main(verbosity=2, argv=sys.argv[:1])
