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


ISSUE_ST_CREATED = 0
ISSUE_ST_PENDING = 1 << 1
ISSUE_ST_DENIED = 1 << 2
ISSUE_ST_PUBLISHED = 1 << 3


class IssueLabel(Base):

    __tablename__ = 't_is_label'

    label_id = Column(BigInteger,
                      primary_key=True,
                      autoincrement=True)
    label_text = Column(String(120),
                        nullable=False)
    label_desc = Column(String(120))
    fore_color = Column(String(16))
    back_color = Column(String(16))
    sort_index = Column(Integer, default=0)
    enabled = Column(Integer, default=1)


class IssueNode(Base):

    __tablename__ = 't_is_node'

    node_id = Column(BigInteger,
                     primary_key=True,
                     autoincrement=True)
    issue_id = Column(BigInteger, 
                      nullable=False)
    parent_node_id = Column(BigInteger, 
                            nullable=False)
    node_type = Column(Integer, 
                       nullable=False)
    content = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    created_user_id = Column(BigInteger,
                             nullable=False)
    updated_user_id = Column(BigInteger)
    status = Column(Integer, 
                    nullable=False,
                    default=ISSUE_ST_CREATED)


class IssueNodeLog(Base):

    __tablename__ = 't_is_node_log'

    log_id = Column(BigInteger,
                    primary_key=True,
                    autoincrement=True)
    action_type = Column(String(30))
    action_desc = Column(Text)
    user_id = Column(BigInteger)
    log_date = Column(DateTime)
    node_id = Column(BigInteger, 
                     nullable=False)


class IssueNodeLabel(Base):

    __tablename__ = 't_is_node_label'

    node_id = Column(BigInteger,
                     nullable=False)
    label_id = Column(BigInteger,
                      nullable=False)
    
