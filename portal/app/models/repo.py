# -*- coding: utf-8 -*-

from sqlalchemy import Sequence, Column, String, Integer, DateTime
from sqlalchemy import ForeignKey, Text, BigInteger
from sqlalchemy import text
from models.helper import engine, orm_session, Base


class Repo(Base):

    __tablename__ = 't_repo'

    local_id = Column(BigInteger, 
                      primary_key=True, 
                      autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    repo_name = Column(String(120), nullable=False)
    local_type = Column(String(30), default='github')
    repo_id = Column(BigInteger)
    full_name = Column(String(120))
    repo_type = Column(String(30))
    repo_desc = Column(String(120))
    is_fork = Column(Integer)
    html_url = Column(String(120))
    ssh_url = Column(String(120))
    git_url = Column(String(120))
    private = Column(Integer, nullable=False, default=0)
    lang = Column(String(30))
    default_branch = Column(String(60))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


# class RepoCommit(Base):

#     __tablename__ = 't_repo_commit'
    
#     local_id = Column(BigInteger,
#                       primary_key=True, 
#                       autoincrement=True)
