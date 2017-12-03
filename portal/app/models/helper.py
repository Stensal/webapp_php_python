# -*- coding: utf-8 -*-

import os, sys

_dir = os.path.dirname(os.path.abspath(__file__))
_appdir = os.path.abspath(os.path.join(_dir, '..'))

if _appdir not in sys.path:
    sys.path.insert(0, _appdir)

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import config


db_url = 'mysql+pymysql://'
db_url += '%(user)s:%(password)s@%(host)s:%(port)s/%(db)s'
db_url = db_url % config.dbinfo

engine = sa.create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)

def orm_session(**kargs):
    return Session(**kargs)

