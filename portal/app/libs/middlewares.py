# -*- coding: utf-8 -*- 

import os, sys


class BlockNonWsRequestMiddleware(object):

    def __init__(self, app, passthrough=None):
        self.app = app
        self.passthrough = passthrough or []

    def deny(self, environ, start_response):
        headers = [('content-type', 'text/plain')]
        start_response('400 websocket only.', headers)
        msg = ('This is a websocket server, ',
               'serves websocket requests only.')
        for line in msg:
            yield line

    def __call__(self, environ, start_response):
        _path = environ['PATH_INFO']
        if self.passthrough:
            for pt in self.passthrough:
                if _path.lower().startswith(pt):
                    return self.app(environ, start_response)
        connection = environ.get('HTTP_CONNECTION', '').lower()
        connection = connection.split(',')
        connection = [c.strip() for c in connection if c.strip()]
        upgrade = environ.get('HTTP_UPGRADE', '').lower()
        if 'upgrade' not in connection or upgrade != 'websocket':
            return self.deny(environ, start_response)
        return self.app(environ, start_response)



class AccessControlMiddleware(object):

    def __init__(self, app, 
                 allow_headers=[],
                 max_age=3600):
        self.app = app
        self.allow_headers = allow_headers or []
        self.max_age = max_age

    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        if method.lower() == 'options':
            return self._request_options(environ, start_response)
        # path = environ['PATH_INFO']
        # if path.lower().endswith('.json'):
        def _start_response(status, headers):
            lkeys = dict([(h[0].lower(), h[0]) for h in headers])
            if 'x-frame-options' not in lkeys:
                headers.append(('X-Frame-Options', 'SAMEORIGIN'))
            name = self.__class__.__name__
            headers.append(('X-Middleware', name))
            return start_response(status, headers)
        return self.app(environ, _start_response)

    def _request_options(self, environ, start_response):
        _key_method = 'HTTP_ACCESS_CONTROL_REQUEST_METHOD'
        _key_headers = 'HTTP_ACCESS_CONTROL_REQUEST_HEADERS'
        req_method = ''
        # if _key_method in environ:
        #     req_method = environ[_key_method]
        req_method = 'GET, POST'
        req_headers = ''
        if _key_headers in environ:
            req_headers = environ[_key_headers]
        headers = [('Access-Control-Allow-Origin', '*'),
                   ('Access-Control-Allow-Methods', req_method),
                   ('Access-Control-Allow-Headers', req_headers),
                   ('Access-Control-Max-Age', '%s' % self.max_age)]
        if self.allow_headers:
            h = ','.join(self.allow_headers)
            headers.append(('Access-Control-Expose-Headers', h))
        start_response('200 OK', headers)
        yield ''


