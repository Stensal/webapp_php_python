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
    return {'title': ''}

@bp.route('/privacy/', methods=['POST', 'GET'])
@jview('privacy.html')
def privacy():
    return {'title': 'Privacy', 'active': 'Privacy'}

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

