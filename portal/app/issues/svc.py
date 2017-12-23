# -*- coding: utf-8 -*- 

import logging
import json
# from collections import namedtuple
from libs.utils import namedtuple
from models.helper import orm_session
from models.issue import IssueLabel, IssueNode
from models.issue import IssueNodeLog, IssueNodeLabel
from models.issue import ISSUE_ST_PUBLISHED
from models.issue import ISSUE_NODE_TYPE_LABELS
from models.issue import ISSUE_NODE_TYPE_STATUS
from models.issue import ISSUE_NODE_TYPE_CONTENT
from models.user import UserInfo, GithubUser
from sqlalchemy import text as text_
from sqlalchemy.orm import aliased
import libs.mysql_helper as my
import config


logger = logging.getLogger(__name__)


def get_labels():
    s = orm_session()
    rs = s.query(IssueLabel).all()
    s.close()
    return rs

def get_label_by_text(label_text):
    s = orm_session()
    rs = s.query(IssueLabel) \
         .filter(IssueLabel.label_text == label_text) \
         .first()
    return rs

def get_label_by_id(label_id):
    s = orm_session()
    rs = s.query(IssueLabel) \
         .filter(IssueLabel.label_id == label_id) \
         .one_or_none()
    return rs

# def _delete_all_labels():
#     s = orm_session()
#     s.query(IssueLabel).delete()
#     s.commit()

def add_label(label_text,
              label_desc=None,
              fore_color=None,
              back_color=None,
              sort_index=None,
              enabled=True):
    if not label_text:
        raise ValueError('label_text')
    elif not isinstance(label_text, str):
        raise TypeError('label_text should be str.')
    elif len(label_text) > 100:
        raise ValueError('too long for label_text.')
    s = orm_session()
    lb = s.query(IssueLabel) \
         .filter(IssueLabel.label_text == label_text) \
         .first()
    if lb:
        # raise ValueError('label_text already exists.')
        return lb
    lb = IssueLabel()
    lb.label_text = label_text
    lb.fore_color = fore_color
    lb.back_color = back_color
    lb.label_desc = label_desc
    lb.enabled = 1 if enabled else 0
    s.add(lb)
    s.commit()
    s.close()
    return lb

def set_label_enabled(label_id, enabled):
    s = orm_session()
    lb = s.query(IssueLabel)\
          .filter(IssueLabel.label_id == label_id) \
          .one_or_none()
    if not lb:
        return
    lb.enabled = 1 if enabled else 0
    s.commit()
    s.close()

def add_default_labels():
    labels = (('bug', 'white', 'red'),
              ('duplicate', '', '#999999'),
              ('enhancement', 'white', '#0066e9'),
              ('help wanted', 'white', 'green'),
              ('invalid', '', 'gray'),
              ('question', 'white', '#f00066'),
              ('wontfix', '', ''),)
    s = orm_session()
    for i, vals in enumerate(labels):
        text, fc, bc = vals
        lb = s.query(IssueLabel) \
              .filter(IssueLabel.label_text == text) \
              .one_or_none()
        if lb:
            continue
        lb = IssueLabel()
        lb.label_text = text
        lb.fore_color = fc
        lb.back_color = bc
        lb.sort_index = i
        s.add(lb)
    s.commit()
    s.close()

def get_nodes(only_root_nodes=True,
              issue_id=None,
              label_id=None,
              page=1, 
              page_size=15):
    if page <= 0:
        page = 0
    if page_size <= 0:
        page_size = 1
    elif page_size > 100:
        page_size = 100

    args = {}
    sql = ['select n.*, ',
           '       t1.labels_json, ',
           '       uc.display_name created_user_name, ',
           # '       uc.avatar_url created_user_avatar, ',
           '       uu.display_name updated_user_name ',
           # '       uu.avatar_url updated_user_avatar ',
           '  from t_is_node n ',
           '  left join t_user_info uc ',
           '    on uc.user_id = n.created_user_id ',
           '  left join t_user_info uu ',
           '    on uu.user_id = n.updated_user_id ',
           "  left join (select t.node_id, "
           "                    '['||group_concat(t.lb)||']' labels_json ",
           "               from (select nl.node_id, ",
           "                     json_object('label_id', nl.label_id, ",
           "                                 'label_text', l.label_text) lb ",
           "                       from t_is_node_label nl, ",
           "                            t_is_label l ",
           '                      where nl.label_id = l.label_id) t ',
           '              group by t.node_id) t1 ',
           '    on t1.node_id = n.node_id ',]

    conds = []

    s = orm_session()
    
    if only_root_nodes:
        conds.append(' n.issue_id = n.node_id ')

    if label_id:
        _cond = (' n.node_id in (select node_id ',
                 '   from t_is_node_label ',
                 '  where label_id=:label_id)')
        conds.append(''.join(_cond))
        args['label_id'] = label_id

    if issue_id:
        _cond = 'issue_id=:issue_id'
        conds.append(_cond)
        args['issue_id'] = issue_id

    if conds:
        sql.append(' where ')
        sql.append(' and '.join(conds))

    if page > 0:
        offset = (page - 1) * page_size
        limit = page_size + 1
        sql.append(' limit :limit offset :offset ')
        args['limit'] = limit
        args['offset'] = offset

    # logger.info('\r\n'.join(sql) % args)

    cur = s.execute(''.join(sql), args)
    # logger.info(cur.keys())
    M = namedtuple('M', cur.keys())

    # rs = rs.all()[offset:offset+limit]
    # items = [t for t in rs]
    items = [M(*vals) for vals in cur]
    _preprocess_node_attrs(items)

    s.close()

    has_more = False
    if page > 0 and len(items) > page_size:
        items = items[:-1]
        has_more = True
    # logger.info([t.issue_id for t in items])
    return items, has_more

def _preprocess_node_attrs(items):
    for t in items:
        if 'labels_json' in t:
            t['labels'] = json.loads(t['labels_json'] or '[]')

def get_issue_labels(node_id):
    '''given any node_id of an issue., return issue's labels.'''
    conn, cur = None, None
    try:
        conn = my.connect(**config.dbinfo)
        cur = conn.cursor()
        sql = ('select l.* from t_is_label l ',
               ' where l.label_id in (select nl.label_id ',
               '   from t_is_node_label nl, t_is_node n ',
               '  where n.node_id=%s ',
               '    and nl.node_id=n.issue_id) ',)
        cur.execute(''.join(sql), (node_id,))
        labels = my.fetchall(cur)
        return labels
    finally:
        if cur: cur.close()
        if conn: conn.close()

def update_issue_labels(node_id, label_ids,
                        user_id=None):
    conn, cur = None, None
    try:
        conn = my.connect(**config.dbinfo)
        cur = conn.cursor()

        sql = 'select issue_id from t_is_node where node_id=%s'
        cur.execute(sql, (node_id,))
        row = my.fetchone(cur)
        if not row or not row.issue_id:
            return
        issue_id = row.issue_id

        # -- create node
        sql = ('insert into t_is_node ',
               '  (issue_id, parent_node_id, node_type, ',
               '   created_at, created_user_id, ',
               '   status) ',
               ' values ',
               '  (%(issue_id)s, %(parent_node_id)s, %(node_type)s, ',
               '   NOW(), %(user_id)s, %(status)s) ',)
        args = {
            'issue_id': issue_id,
            'parent_node_id': node_id,
            'node_type': ISSUE_NODE_TYPE_LABELS,
            'user_id': user_id,
            'status': ISSUE_ST_PUBLISHED
        }
        cur.execute(''.join(sql), args)
        new_node_id = conn.insert_id()

        # -- create log
        sql = ('insert into t_is_node_log ',
               ' (action_type, action_desc, user_id, ',
               '  log_date, node_id) ',
               ' values ',
               ' (%(action_type)s, %(action_desc)s, %(user_id)s, ',
               '  NOW(), %(node_id)s) ',)
        args = {
            'action_type': 'set_labels',
            'action_desc': None,
            'user_id': user_id,
            'node_id': new_node_id
        }
        cur.execute(''.join(sql), args)

        # -- remove existing labels --
        sql = ('delete from t_is_node_label ',
               ' where node_id=%s',)
        cur.execute(''.join(sql), (issue_id,))

        # -- set labels --
        sql = ('insert into t_is_node_label ',
               ' (node_id, label_id) values (%s, %s) ',)
        label_ids = list(set([lbid for lbid in label_ids if lbid]))
        if label_ids:
            args_list = [(new_node_id, lbid) for lbid in label_ids]
            cur.executemany(''.join(sql), args_list)
            args_list = [(issue_id, lbid) for lbid in label_ids]
            cur.executemany(''.join(sql), args_list)

        # --
        conn.commit()
        return new_node_id
    finally:
        if cur: cur.close()
        if conn: conn.close()

def update_node_content(node_id, content,
                        user_id=None):
    conn, cur = None, None
    try:
        conn = my.connect(**config.dbinfo)
        cur = conn.cursor()

        # -- create log
        sql = ('insert into t_is_node_log ',
               ' (action_type, action_desc, user_id, ',
               '  log_date, node_id) ',
               ' values ',
               ' (%(action_type)s, %(action_desc)s, %(user_id)s, ',
               '  NOW(), %(node_id)s) ',)
        args = {
            'action_type': 'update_content',
            'action_desc': None,
            'user_id': user_id,
            'node_id': node_id
        }
        cur.execute(''.join(sql), args)

        # -- update content
        sql = ('update t_is_node ',
               '   set content=%(content)s, ',
               '       updated_at=NOW(), ',
               '       updated_user_id=%(user_id)s ',
               ' where node_id=%(node_id)s ',)
        args = {
            'node_id': node_id,
            'user_id': user_id,
            'content': content
        }
        cur.execute(''.join(sql), args)
        updated = cur.rowcount > 0
        
        conn.commit()
        return updated
    finally:
        if cur: cur.close()
        if conn: conn.close()

