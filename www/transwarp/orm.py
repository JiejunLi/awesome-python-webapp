#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Alljun Lee'

'''
Database operation module. This module is independent with web module
'''

import logging
from . import db

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    db.create_engine('www-data', 'www-data', 'test')
    db.update('drop table if exist user')
    db.update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    import doctest
    doctest.testmod()
