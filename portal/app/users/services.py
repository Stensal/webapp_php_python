# -*- coding: utf-8 -*-

import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))
_appdir = os.path.abspath(os.path.join(_dir, '..'))

import logging

modpath = os.path.relpath(os.path.abspath(__file__), _appdir)
logger = logging.getLogger(modpath)

from models.helper import orm_session
from models.user import UserInfo, UserLog, GithubUser
from models.repo import Repo


def sync_user_repos(user_id, repos):
    return True

