# -*- coding: utf-8-unix -*-

import os, sys
import logging
import time

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.append(_dir)

import sqlalchemy
import models.user
import models.repo
from models.helper import engine, Base


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


