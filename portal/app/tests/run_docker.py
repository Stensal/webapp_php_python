#!/usr/bin/env python
# -*- coding: utf-8-unix -*-

import os
_dir = os.path.dirname(os.path.abspath(__file__))
_dir = os.path.abspath(os.path.join(_dir, '..'))
os.system(r"cd %(pwd)s && ((docker image ls | grep portal_web) || docker build -t portal_web . ) && docker run --rm -ti -v %(pwd)s:/data portal_web python3 /data/tests/main.py" % {'pwd': _dir})

