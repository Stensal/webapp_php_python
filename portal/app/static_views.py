#-*- coding: utf-8 -*-

import os
import sys

_dir = os.path.dirname(os.path.abspath(__file__))

from flask import Blueprint, request, redirect, abort
from flask import make_response, render_template
from flask import send_file, send_from_directory
from ui import jview, json_view
import config


static_bp = Blueprint('static_bp', __name__, template_folder='templates')


def is_static_file(filepath):
    folder = os.path.abspath(os.path.join(_dir, 'static'))
    filepath = os.path.abspath(filepath)
    prefix = os.path.commonprefix([folder, filepath])
    return prefix == folder

def _h403():
    resp = make_response('403 access denied.')
    resp.status_code = 403
    return resp

def _h404():
    resp = make_response('404 not found.')
    resp.status_code = 404
    return resp

@static_bp.route('/<ver>/<path:relpath>', methods=['POST', 'GET'])
def versioned_static_file(ver, relpath):
    filepath = os.path.abspath(os.path.join(_dir, relpath))
    if not is_static_file(filepath):
        return _h404()
    elif not os.path.isfile(filepath):
        return _h404()
    folder = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    return send_from_directory(folder, filename)

@static_bp.route('/', methods=['GET', 'POST'])
def readme():
    return u'virtual mapping module for static files.'


