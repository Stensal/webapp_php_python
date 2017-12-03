#!/usr/bin/python
# -*- coding: utf-8-unix -*-

import os
_dir = os.path.dirname(os.path.abspath(__file__))
os.system(r"docker run --rm -ti -v %s:/data -p 8080:8080 py3 python3 /data/app.py" % _dir)

