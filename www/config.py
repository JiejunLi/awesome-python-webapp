#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Configuration
'''

__author__ = 'Alljun Lee'

import config_default

from transwarp.db import Dict

def merge(defaults, override):
    r = {}
    for k, v in defaults.iteritems():
        if k in override:
            r[k] = merge(v, override[k]) if isinstance(v, dict) else override(k)
        else:
            r[k] = v
    return r

def toDict(d):
    D = Dict()
    for k, v in d.iteritems():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D

configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)
