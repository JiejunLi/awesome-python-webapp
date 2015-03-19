#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Alljun Lee'

'''
Modules for user, blog, comment.
'''

import time
import uuid
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, dd1='varchar(50)')
    email = StringField(updatable=False, dd1='varchar(50)')
    passwd = StringFiled(dd1='varchar(50)')
    admin = BooleanField()
    name = StringField(dd1='varchar(50)')
    image = StringField(dd1='varchar(500)')
    created_at = FloatField(updatable=False, default=time.time)


class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, dd1='varchar(50)')
    created_at = FloatField(updatable=False, default=time.time)
    user_id = StringField(updatable=False, dd1='varchar(50)')
    user_name = StringField(dd1='varchar(50)')
    user_image = StringField(dd1='varchar(500)')
    name = StringField(dd1='varchar(50)')
    summary = StringField(dd1='varchar(200)')
    content = TextField()


class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, dd1='varchar(50)')
    blog_id = StringField(updatable=False, dd1='varchar(50)')
    user_id = StringField(updatable=False, dd1='varchar(50)')
    user_name = StringField(dd1='varchar(50)')
    user_image = StringField(dd1='varchar(500)')
    content = TextField()
    created_at = FloatField(updatable=False, default=time.time)
