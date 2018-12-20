#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from flask import current_app

class Account(object):
    
    __slots__ = ('account_id', 'account_type', 'account_value', 'create_time', 'user')
     
    def __init__(self, **kw):
        
        Account._connection    = MongoClient(current_app.config['MONGODB_DNS'])
        Account._db            = self._connection.timelog
        Account._collection    = self._db.account
        
        Account._collection.create_index('value', unique=True);
        Account._collection.create_index('user', unique=True);
        
        for item in kw:
            setattr(self, item, kw[item])

    def save(self):
        
        if getattr(self, 'account_id', None) == None:
            self.account_id = Account._collection.insert_one({
                'type'  : self.account_type,
                'value' : self.account_value,
                'user'  : self.user.toMongoJson()
            }).inserted_id
        else:
            Account._collection.save({
                '_id'   : self.account_id,
                'type'  : self.account_type,
                'value' : self.account_value,
                'user'  : self.user.toMongoJson()
            })
        return self
    
    def __call__(self):
        pass
    