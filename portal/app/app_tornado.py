#-*- coding: utf-8 -*-

import os, sys

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)


from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop

import config
from app import app
from libs.middlewares import AccessControlMiddleware


if __name__ == '__main__':
    app.wsgi_app = AccessControlMiddleware(app.wsgi_app)

    if not config.cli.do_import_test:
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(config.port)
        IOLoop.instance().start()
