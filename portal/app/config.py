# -*- coding: utf-8 -*-

import os, sys, socket, argparse, json, yaml
import logging
import six

logger_name = os.path.splitext(os.path.basename(__file__))[0]
logger = logging.getLogger(logger_name)

_ap = argparse.ArgumentParser()
_ap.add_argument('-c', '--config',
                 metavar="NAME",
                 help='configuration name, eg. "dev"',
                 dest='config_name',
                 action='store')
_ap.add_argument('-p', '--port',
                 metavar='PORT', dest='port', type=int,
                 action='store', default=8080)
_ap.add_argument('-t', '--do-import-test',
                 action='store_const',
                 const=True)
_cli = _ap.parse_args()

_dir = os.path.dirname(os.path.abspath(__file__))

_debug_ = 'debug' in os.environ.get('COMPUTERNAME', '').lower()


class _Conf(object):

    def __init__(self, conf_name):
        self._debug_ = _debug_ # sys.platform != 'linux2'
        self.deploy_flag = 'debug' if self._debug_ else 'deploy'
        self._conf = {}
        self._load_conf(conf_name)
        self.port = _cli.port
        self.cli = _cli
        self.PY2 = six.PY2
        self.PY3 = six.PY3

    def _load_conf(self, name):
        name = name or 'dev'
        _name, _ext = os.path.splitext(name)
        if _ext and _ext.lower() != '.yaml':
            _name = name
        filenames = (_name + '.yaml',
                     _name + '.' + self.deploy_flag + '.yaml')
        conf = {}
        for fname in filenames:
            conf_file = os.path.join(_dir, 'conf', fname)
            conf_file = os.path.abspath(conf_file)
            if not os.path.isfile(conf_file):
                continue
            logger.debug(' * conf <- %s' % os.path.relpath(conf_file, _dir))
            with open(conf_file, 'rb') as f:
                _d = yaml.load(f.read())
                if _d:
                    conf.update(_d)
        if not conf:
            raise Exception('Unable load config "%s".' % name)
        self._conf.update(conf)

    def has(self, key):
        return key in self._conf

    def __getattr__(self, key):
        '''
        https://docs.python.org/2/reference/datamodel.html

        Called when an attribute lookup has not found 
        the attribute in the usual places (i.e. it is not 
        an instance attribute nor is it found in 
        the class tree for self). 
        name is the attribute name. This method should 
        return the (computed) attribute value or 
        raise an AttributeError exception.
        '''
        if key in self._conf:
            v = self._conf[key]
            if isinstance(v, dict) and len(v.keys()) == 2:
                if 'debug' in v and 'deploy' in v:
                    return v[self.deploy_flag]
            return v
        raise AttributeError(key)


sys.modules[__name__] = _Conf(_cli.config_name)

