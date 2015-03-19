#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Alljun Lee'

'''
Database operation module.
'''

import logging
import threading

class DBError(Exception):
    pass

class _LasyConnection(object):
    '''
    Lasy connection
    '''
    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            connection = engine.connect()
            logging.info('open connection <%s>...' % hex(id(connection)))
            self.connection = connection
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            connection = self.connection
            self.connection = None
            logging.info('close connection <%s>...' % hex(id(connection)))
            connection.close()

class _DbCtx(threading.local):
    '''
    Thread local object that holds connection info.
    '''
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
        logging.info('open lazy connection...')
        self.connection = _LasyConnection()
        self.transactions = 0

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        '''
        Return cursor
        '''
        return self.connection.cursor()

class _TransactionCtx(object):
    '''
    _TransactionCtx object that can handle transctions.

    with _TransactionCtx():
        pass
    '''

    def __enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn = True
        _db_ctx.transactions = _db_ctx.transactions + 1
        logging.info('begin transaction...' if _db_ctx.transactions==1 else 'join current transaction...')
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        _db_ctx.transactions = _db_ctx.transactions - 1
        try:
            if _db_ctx.transactions == 0:
                self.commit()
            else:
                self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()
    def commit(self):
        global _db_ctx
        logging.info('commit transaction...')
        try:
            _db_ctx.connection.commit()
            logging.info('commit ok.')
        except:
            logging.warning('commit failed try rollback...')
            _db_ctx.connection.rollback()
            logging.warning('rollback ok.')
            raise

    def rollback(self):
        global _db_ctx
        logging.warning('rollback transaction...')
        _db_ctx.connection.rollback()
        logging.info('rollback ok.')

def transaction():
    '''
    Create a transaction object so can use with statement:

    with transaction():
        pass
    '''
    return _TransactionCtx()

# thread-local db context:
_db_ctx = _DbCtx()

@with_connection
def _update(sql, *args):
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')
    logging.info('SQL: %s, ARGS: %s' % (sql, args))
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, args)
        r = cursor.rowcount
        if _db_ctx.transaction == 0:
            # no transaction enviroment:
            logging.info('auto commit')
            _db_ctx.connection.commit()
        return r
    finally:
        if cursor:
            cursor.close()

def update(sql, *args):
    '''
    Execute update SQL.

    >>>u1 = dict(id=1000, name='AlljunLee', email='lijj@cloud-times.com', passwd='abc123', last_modified=time.time())
    >>>insert('user' **u1)
    '''
    return _update(sql, *args)

# global engine object:
engine = None

class _Engine(object):

    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()

def create_engine(user, passwd, database, host='127.0.0.1', port=3306, **kw):
    '''
    Init db connection infomation.
    '''
    import mysql.connector
    global engine

    if engine is not None:
        raise DBError('Engine is already initialized.')

    params = dict(user=user, passwd=passwd, database=database, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    params.update(kw)
    params['buffered'] = True

    engine = _Engine(lambda: mysql.connector.connect(**params))
    # test connection...
    logging.info('Init mysql engine <%s> ok.' % hex(id(engine)))

if __name__ == '__main__':
    logging.basicConfig(level = logging.DEBUG)
    create_engine('www-data', 'www-data', 'test')
    update('drop table if exists user')
    update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    import doctest
    doctest.testmod()
