#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient, errors
from flask import current_app

class User(object):
    
    __slots__ = ('user_id', 'user_name', 'user_password')
     
    def __init__(self, **kw):
        
        User._connection    = MongoClient(current_app.config['MONGODB_DNS'])
        User._db            = self._connection.timelog
        User._collection    = self._db.user
        
        for item in kw:
            setattr(self, item, kw[item])

    def toMongoJson(self):
        
        return {
            '_id'           : getattr(self, 'user_id', None),
            'name'          : self.user_name,
            'password'      : self.user_password,
        };
        
    def save(self):
        
        if getattr(self, 'user_id', None) == None:
            self.user_id    = User._collection.insert_one({
                'name'      : self.user_name,
                'password'  : self.user_password
            }).inserted_id
        else:
            User._collection.save({
                '_id'       : self.user_id,
                'name'      : self.user_name,
                'password'  : self.user_password
            })
        return self
    
    def __call__(self):
        pass