# -*- coding: utf-8 -*-

import os, sys
import unittest as ut

_dir = os.path.dirname(os.path.abspath(__file__))
_rootdir = os.path.abspath(os.path.join(_dir, '../'))
if _rootdir not in sys.path:
    sys.path.append(_rootdir)

from app import app


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
