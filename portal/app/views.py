#-*- coding: utf-8 -*-

import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))

from flask import Blueprint, request, redirect, abort
from flask import make_response, render_template
from flask import send_file
from ui import jview, json_view
import config
import libs.mysql_helper as my


bp = Blueprint('root_bp', __name__, template_folder='templates')


@bp.route('/', methods=['POST', 'GET'])
@jview('index.html')
def index():
    return {}

@bp.route('/demo/', methods=['POST', 'GET'])
@jview('demo.html')
def demo():
    return {'title': 'Demo', 'active': 'Demo'}

@bp.route('/products/', methods=['POST', 'GET'])
@jview('products.html')
def products():
    return {'title': 'Products', 'active': 'Products'}

@bp.route('/issues/', methods=['POST', 'GET'])
@jview('issues.html')
def issues():
    return {'title': 'Issues', 'active': 'Issues'}

@bp.route('/db_test/', methods=['POST', 'GET'])
@json_view
def do_a_db_test():
    conn, cur = None, None
    rows = []
    try:
        conn = my.connect(**config.dbinfo)
        cur = conn.cursor()
        cur.execute("select now() d, '中文' c")
        rows = cur.fetchall()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return rows


