#-*- coding: utf-8 -*-


class Abort(Exception):
    
    def __init__(self, *args):
        msg = args[0] if args else None
        self.msg = msg
        self.message = msg
    
