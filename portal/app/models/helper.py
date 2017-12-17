# -*- coding: utf-8 -*-

import os, sys

_dir = os.path.dirname(os.path.abspath(__file__))
_appdir = os.path.abspath(os.path.join(_dir, '..'))

if _appdir not in sys.path:
    sys.path.insert(0, _appdir)

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config


db_url = 'mysql+pymysql://'
db_url += '%(user)s:%(password)s@%(host)s:%(port)s/%(db)s'
db_url = db_url % config.dbinfo

_echo = ('TEST_MODE' not in os.environ) or False
engine = sa.create_engine(db_url, echo=_echo)
Session = sessionmaker(bind=engine)

def orm_session(**kargs):
    return Session(**kargs)

Base = declarative_base()

