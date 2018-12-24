# -*- coding: utf-8 -*-

from pymongo import MongoClient
import bson
#from flask import current_app

class Client(object):
    
    __slots__ = ('_connection', '_db', '_collection')
    
#     def __init__(self, connection = MongoClient(current_app.config['MONGODB_DNS']), db = current_app.config['DB']):
    def __init__(self, connection, db):
        self._connection    = connection
        self._db            = self._connection[db]
        self._collection    = self._db['account']
        self._collection.create_index('account_value', unique=True);
#         self._collection.create_index('user', unique=True);
        
    def findByAccountValue(self, account_value):
        return self._collection.find_one({'account_value' : account_value})
    
    
    def save(self, data):
        account                 = {
            'account_type'      : data['account_type'],
            'account_value'     : data['account_value'],
            'user'              : [{
                'user_name'     : data['user']['user_name'],
                'user_password' : data['user']['user_password']
            }]
        }
        if '_id' in data:
            account['_id']           = data['_id']
        self._collection.save(account)
        return account
        