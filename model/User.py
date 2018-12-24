# -*- coding: utf-8 -*-

from pymongo import MongoClient
#from flask import current_app

class Client(object):
    
    __slots__ = ('_connection', '_db', '_collection')
    
    def __init__(self, connection = MongoClient(current_app.config['MONGODB_DNS']), db = current_app.config['DB'], collection ='user'):
        self._connection    = connection
        self._db            = self._connection[db]
        self._collection    = self._db[collection]
        self._collection.create_index('user.account.value', unique=True);
        
    def findByAccountValue(self, account_value):
        return self._collection.find_one({'user.account.value' : account_value})    
    
    def save(self, data):
        user                    = {
            'name'              : data['name'],
            'password'          : data['password'],
            'account'           : []
        }
        
        for i in data['accounts']:
            user['account'][i]  = {
                'type'          : data['accounts'][i]['type'],
                'value'         : data['accounts'][i]['value'] 
            }
        
        if '_id' in data:
            user['_id'] = data['_id']
            
        self._collection.save(user)
        
        return user
        