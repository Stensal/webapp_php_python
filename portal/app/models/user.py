# -*- coding: utf-8 -*-

import os, sys

_dir = os.path.dirname(os.path.abspath(__file__))
_appdir = os.path.abspath(os.path.join(_dir, '..'))

if _appdir not in sys.path:
    sys.path.insert(0, _appdir)

import datetime
import uuid
from sqlalchemy import Sequence, Column, String, Integer, DateTime
from sqlalchemy import ForeignKey, Text, BigInteger
from sqlalchemy import text
from models.helper import engine, orm_session, Base
from models.helper import JSONSerializable


class UserInfo(Base, JSONSerializable):

    __tablename__ = 't_user_info'
    
    user_id = Column(BigInteger, 
                     primary_key=True, 
                     autoincrement=True)
    unified_id = Column(String(60), 
                        unique=True,
                        nullable=False)
    display_name = Column(String(120), 
                          nullable=False)
    first_name = Column(String(60))
    last_name = Column(String(60))
    org_name = Column(String(200))
    reg_date = Column(DateTime, 
                      nullable=False,
                      default=datetime.datetime.now)


class UserPriv(Base, JSONSerializable):

    __tablename__ = 't_user_priv'

    pair_id = Column(BigInteger, 
                     nullable=False,
                     autoincrement=True,
                     primary_key=True)
    user_id = Column(BigInteger, 
                     nullable=False)
    priv_code = Column(String(60), 
                       nullable=False)


class GithubUser(Base, JSONSerializable):

    __tablename__ = 't_github_user'

    local_id = Column(BigInteger, 
                      primary_key=True,
                      autoincrement=True)
    user_id = Column(BigInteger, 
                     nullable=False)
    github_id = Column(BigInteger,
                       unique=True,
                       nullable=False)
    login_name = Column(String(120))
    html_url = Column(String(120))
    avatar_url = Column(String(120))
    profile_json = Column(Text)
    token_json = Column(Text)
    last_update = Column(DateTime, 
                         nullable=False,
                         default=datetime.datetime.now,
                         onupdate=datetime.datetime.now)


class UserLog(Base, JSONSerializable):

    __tablename__ = 't_user_log'

    local_id = Column(BigInteger, nullable=False)
    log_id = Column(BigInteger, primary_key=True,
                    autoincrement=True)
    action_name = Column(String(120), nullable=False)
    log_date = Column(DateTime, nullable=False)
    ua = Column(Text)
    ip = Column(String(30))
    remark = Column(String(120))


# Base.metadata.create_all(bind=engine, checkfirst=True)


if __name__ == '__main__':
    sess = orm_session(autocommit=False)
    # user = UserInfo(unified_id=uuid.uuid4().hex)
    # sess.begin()
    # sess.add(user)
    # sess.commit()
    # guser = sess.query(GithubUser.user_id) \
    #             .filter_by(github_id=8371274).first()
    # if not guser:
    #     user = UserInfo(unified_id=uuid.uuid4().hex)
    #     sess.add(user)
    #     sess.commit()
    #     guser = GithubUser(user_id=user.user_id,
    #                        github_id=8371274)
    #     sess.add(guser)
    #     sess.commit()
    #     print('==>', user.user_id, guser.local_id)
    # else:
    #     print('--<', guser)


