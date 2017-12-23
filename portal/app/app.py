#-*- coding: utf-8 -*-

import os, sys
import logging

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.append(_dir)

logging_conf = {
    'level': logging.DEBUG,
    'format': '%(name)6s - [%(levelname)s]: %(message)s'
}
logging.basicConfig(**logging_conf)

from flask import Flask, redirect, request
from flask import render_template, make_response
from ui import jview, json_view
from session import SessionInterface
from libs.middlewares import AccessControlMiddleware
import config


app = Flask(__name__, template_folder='templates')
app.session_interface = SessionInterface()
app.debug = True


blueprints = (

    # users area, signup/profile edit/logout, etc.
    ('users.views.bp', '/users'),

    # issues
    ('issues.views.bp', '/issues'),

    # 带版本的静态文件
    ('static_views.static_bp', '/v'),

    # 首页
    ('views.bp', ''),
)

for mod_path, mount_point in blueprints:
    parts = mod_path.split('.')
    _path = '.'.join(parts[:-1])
    bp_name = parts[-1]
    if config.PY3:
        from importlib import import_module
        mod = import_module(_path)
    else:
        mod = __import__(_path, None, None, [bp_name], -1)
    bp = getattr(mod, bp_name)
    app.register_blueprint(bp, url_prefix=mount_point)


if __name__ == '__main__':
    host = ('0.0.0.0', config.port)
    # app.wsgi_app = SessionMiddleware(app.wsgi_app)
    app.wsgi_app = AccessControlMiddleware(app.wsgi_app)
    if not config.cli.do_import_test:
        logging.debug('listening at %s:%d...' % host)
        app.run(host=host[0], port=host[1], debug=True)


