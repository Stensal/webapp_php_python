# -*- coding: utf-8-unix -*-

import os, sys
import logging
import time

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.append(_dir)

import uuid
import sqlalchemy
import models.user
from models.user import UserInfo, GithubUser
import models.repo
import models.issue
from models.helper import engine, Base, orm_session
import issues.svc
import users.services
import users.privs


retry = 10
while retry > 0:
    c = None
    try:
        c = engine.connect()
        break
    except sqlalchemy.exc.OperationalError:
        time.sleep(2.0)
        continue
    finally:
        if c:
            c.close()
        retry -= 1

Base.metadata.create_all(bind=engine, checkfirst=True)
# -- create 1st user --

def create_1st_user():
    pass

create_1st_user()
users.services.add_github_user_priv('smallfz', 
                                    users.privs.PRIV_SUPER_ADMIN.code)
issues.svc.add_default_labels()

