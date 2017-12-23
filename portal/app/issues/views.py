# -*- coding: utf-8 -*-

import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))
_appdir = os.path.abspath(os.path.join(_dir, '..'))

import logging
import re
import datetime
import json
from flask import Blueprint, request, redirect, abort
from flask import make_response, render_template
from flask import send_file, session, url_for
from ui import jview, json_view
import config
import libs.py6 as py6
from libs.app_exp import Abort
from libs.utils import json_dumps, _int
from users.helper import login_required, denied, user_cache
from models.helper import orm_session
from models.user import UserInfo, UserLog, GithubUser
from models.issue import IssueNode, IssueNodeLog, IssueNodeLabel
from models.issue import ISSUE_NODE_TYPE_LABELS
from models.issue import ISSUE_NODE_TYPE_CONTENT
from models.issue import ISSUE_NODE_TYPE_STATUS
from models.issue import ISSUE_ST_PUBLISHED, ISSUE_ST_CREATED
from users.privs import PRIV_SUPER_ADMIN, PRIV_ISSUE
import users.services
import issues.svc as svc
import mistune


modpath = os.path.relpath(os.path.abspath(__file__), _appdir)
logger = logging.getLogger(modpath)

bp = Blueprint('issue_bp', __name__, template_folder='templates')


@bp.route('/')
@jview('issues.html')
def issues_index():
    # return {
    #     'title': 'Issues', 
    #     'ui_components_nav_active': 'issues'
    # }
    return redirect(url_for('.issues_react_app'))

@bp.route('/app/')
@bp.route('/app/<path:route_path>')
@jview('issues.html')
def issues_react_app(*args, **kargs):
    return {
        'title': 'Issues', 
        'ui_components_nav_active': 'issues',
        'router_path': kargs.get('router_path', '')
    }

@bp.route('/conf.<fmt>', methods=['GET', 'POST'])
@json_view
def get_issue_app_conf(fmt):
    if fmt not in ('json',):
        return abort(404)
    user = session.user
    # github_user = None
    # if user.authenticated:
    #     github_user = user.user_info['github_user']
    return {
        'user': user,
        'is_admin': user.has_priv(PRIV_ISSUE | PRIV_SUPER_ADMIN)
    }

@bp.route('/labels.<fmt>', methods=['GET', 'POST'])
@json_view
def get_labels(fmt):
    if fmt not in ('json',):
        return abort(404)
    return svc.get_labels()

@bp.route('/nodes.<fmt>', methods=['GET', 'POST'])
@json_view
def get_issue_nodes(fmt):
    if fmt not in ('json',):
        return abort(404)
    args = request.args
    if request.method == 'POST':
        args = request.form
    label_id = _int(args.get('label_id', ''))
    if label_id < 0:
        label_id = 0
    page = _int(args.get('page', ''))
    page_size = _int(args.get('page_size', ''))
    if page < 1:
        page = 1
    if page_size <= 0:
        page_size = 15
    elif page_size > 100:
        page_size = 100
    nodes, has_more = svc.get_nodes(page=page,
                                    page_size=page_size,
                                    label_id=label_id,
                                    only_root_nodes=True)
    # logger.info(nodes[0] if nodes else None)
    label = None
    if label_id > 0:
        label = svc.get_label_by_id(label_id)
    return {
        'label': label,
        'nodes': nodes,
        'has_more': has_more,
        'page': page,
        'page_size': page_size
    }

@bp.route('/nodes/add.<fmt>', methods=['POST'])
@json_view
@login_required
def add_new_issue_node(fmt):
    if fmt not in ('json',):
        return abort(404)
    user = session.user
    args = request.args
    if request.method == 'POST':
        args = request.form
    # node_type = _int(args.get('node_type', ''))
    # node_type = node_type or ISSUE_NODE_TYPE_CONTENT
    title = args.get('title', '') or None
    content = args.get('content', '') or None
    issue_id = _int(args.get('issue_id', ''))
    parent_node_id = _int(args.get("parent_node_id", ''))
    status = _int(args.get('status', ''))
    labels = args.get('labels', '')
    label_ids = re.findall(r'\d+', labels, re.I|re.S)
    label_ids = list(set(map(int, label_ids)))
    # ---
    result, msg = False, ''
    node = None
    try:
        now = datetime.datetime.now()
        node = IssueNode()
        node.title = title
        node.created_at = now
        node.created_user_id = user.user_id
        node.node_type = ISSUE_NODE_TYPE_CONTENT
        node.issue_id = issue_id if issue_id > 0 else 0
        node.parent_node_id = parent_node_id \
                              if parent_node_id > 0 \
                                 else 0
        node.content = content
        node.status = status or ISSUE_ST_PUBLISHED


        # if node_type == ISSUE_NODE_TYPE_CONTENT:
        #     if issue_id and not parent_node_id:
        #         return abort(400)
        #     elif not issue_id and parent_node_id:
        #         return abort(400)
        #     label_ids = []

        # elif node_type == ISSUE_NODE_TYPE_LABELS:
        #     if not label_ids:
        #         return abort(400)
        #     if not parent_node_id or not issue_id:
        #         return Abort(400)

        # elif node_type == ISSUE_NODE_TYPE_STATUS:
        #     # not implemented yet.
        #     return abort(400)
        # else:
        #     # not implemented yet.
        #     return abort(400)

        s = orm_session()
        s.add(node)
        s.commit()
        node_id = node.node_id

        if not node.issue_id:
            node.issue_id = node_id
            issue_id = node_id
            s.commit()
        
        # if label_ids:
        #     s.query(IssueNodeLabel) \
        #      .filter(IssueNodeLabel.node_id == issue_id) \
        #      .delete()
        #     for label_id in label_ids:
        #         lb = IssueNodeLabel()
        #         lb.node_id = issue_id
        #         lb.label_id = label_id
        #         s.add(lb)

        s.commit()
        result = True

        if label_ids:
            svc.update_issue_labels(node_id, label_ids,
                                    user_id=user.user_id)

    except Abort as e:
        msg = e.msg
    return {
        'result': result,
        'msg': msg,
        'node': node
    }

@bp.route('/nodes/node/<int:node_id>/update_content.<fmt>', 
          methods=['POST'])
@json_view
@login_required
def update_issue_node_content(node_id, fmt):
    if not node_id or node_id <= 0:
        return abort(404)
    if fmt not in ('json',):
        return abort(404)
    args = request.args
    if request.method == 'POST':
        args = request.form
    content = args.get('content', '') or None
    s = orm_session()
    node = s.query(IssueNode) \
            .filter(IssueNode.node_id == node_id) \
            .one_or_none()
    if not node:
        return abort(404)
    # -- 
    user = session.user
    is_admin = user.has_priv(PRIV_ISSUE | PRIV_SUPER_ADMIN)
    if not is_admin and node.user_id != user.user_id:
        return abort(403)
    
    # --
    result = svc.update_node_content(node_id, content,
                                     user_id=user.user_id)
    return {
        'result': result,
        'msg': ''
    }

@bp.route('/nodes/node/<int:node_id>/set_labels.<fmt>', 
          methods=['POST'])
@json_view
@login_required
def update_issue_labels(node_id, fmt):
    if not node_id or node_id <= 0:
        return abort(404)
    if fmt not in ('json',):
        return abort(404)
    args = request.args
    if request.method == 'POST':
        args = request.form
    label_ids = args.get('labels', '')
    label_ids = re.findall(r'\d+', label_ids, re.I|re.S)
    label_ids = list(set(map(int, label_ids)))
    
    user = session.user
    result, msg = False, ''
    current_labels = []
    try:
        result = svc.update_issue_labels(node_id, label_ids,
                                         user_id=user.user_id)
        current_labels = svc.get_issue_labels(node_id)
    except Abort as e:
        msg = e.msg
    return {
        'result': result,
        'msg': msg,
        'labels': current_labels
    }

@bp.route('/nodes/issue/<int:issue_id>.json', 
          methods=['GET', 'POST'])        
@json_view
def get_issue_full_thread_json(issue_id):
    nodes = []
    if issue_id:
        nodes, _ = svc.get_nodes(only_root_nodes=False,
                                 issue_id=issue_id,
                                 page=0)
    return {
        'nodes': nodes
    }

@bp.route('/md_to_html.<fmt>', methods=['POST'])
@json_view
def md_to_html(fmt):
    if fmt not in ('json',):
        return abort(404)
    args = request.args
    if request.method == 'POST':
        args = request.form
    text = args.get('text', '')
    _html = mistune.markdown(text)
    return {
        'html': _html
    }

