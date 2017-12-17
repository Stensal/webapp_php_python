# -*- coding: utf-8 -*-

import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))
_appdir = os.path.abspath(os.path.join(_dir, '..'))

import logging

modpath = os.path.relpath(os.path.abspath(__file__), _appdir)
logger = logging.getLogger(modpath)

import datetime, time
from libs.app_exp import Abort
from libs.utils import json_dumps, _date_iso8601
from sqlalchemy.sql.expression import tuple_
from models.helper import orm_session
from models.user import UserInfo, UserLog, GithubUser
from models.repo import Repo


def update_repo(r, repo_dict):
    r.repo_name = repo_dict['name']
    r.local_type = 'github'
    r.repo_id = repo_dict['id']
    r.full_name = repo_dict['full_name']
    r.repo_type = None
    r.repo_desc = repo_dict['description']
    r.is_fork = 1 if repo_dict['fork'] else 0
    r.html_url = repo_dict['html_url']
    r.ssh_url = repo_dict['ssh_url']
    r.git_url = repo_dict['git_url']
    r.private = 1 if repo_dict['private'] else 0
    r.lang = repo_dict['language']
    r.default_branch = repo_dict['default_branch']
    r.created_at = _date_iso8601(repo_dict['created_at'])
    r.updated_at = _date_iso8601(repo_dict['updated_at'])
    r.repo_json = json_dumps(repo_dict)
    return r

def make_repo(repo_dict, user_id=None):
    '''convert a dict to model Repo object.'''
    r = Repo()
    if user_id:
        r.user_id = user_id
    update_repo(r, repo_dict)
    return r

def sync_user_repos(user_id, repos):
    if repos is None or not isinstance(repos, (list, tuple)):
        raise ValueError('repos should be a list or tuple.')
    repos_dates = dict([(r['id'], _date_iso8601(r['updated_at'])) \
                          for r in repos])
    repos_d = dict([(r['id'], r) for r in repos])
    s = orm_session()
    db_repos = get_user_repos(user_id, orm_s=s)
    db_ids = [r.repo_id for r in db_repos]
    del_items = [r for r in db_repos if r.repo_id not in repos_d]
    new_items = [make_repo(r, user_id=user_id) \
                 for r in repos if r['id'] not in db_ids]
    update_items = [update_repo(r, repos_d[r.repo_id]) \
                    for r in db_repos \
                    if r.repo_id in repos_d \
                    and r.updated_at < repos_dates[r.repo_id]]
    # logger.info('%s items deleted.' % len(del_items))
    # logger.info('%s items added.' % len(new_items))
    # logger.info('%s items updated.' % len(update_items))
    if del_items:
        del_ids = [r.local_id for r in del_items]
        s.query(Repo.local_id) \
         .filter(Repo.user_id == user_id) \
         .filter(Repo.local_id.in_(del_ids)) \
         .delete(synchronize_session=False)
    if new_items:
        s.add_all(new_items)
    if del_items or new_items or update_items:
        s.commit()
    return get_user_repos(user_id, orm_s=s)

def get_user_repos(user_id, orm_s=None):
    orm_s = orm_s or orm_session()
    db_repos = orm_s.query(Repo) \
                .filter(Repo.user_id == user_id) \
                .all()
    return db_repos

