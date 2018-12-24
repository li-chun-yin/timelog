# -*- coding: utf-8 -*-

from model.client import Client

def collection():
    accounts = Client.DB['account']
    accounts.create_index('value', unique=True);
    accounts.create_index('user', unique=True);
    return accounts

class Repository(object):
    
    def findByAccountValue(self, account_value):
        cursor     = collection().find({account_value : account_value})
        return cursor[0]
    
class Entity(object):
    
    __slots__ = ()
     
    def __init__(self, **kw):
        
        for item in kw:
            setattr(self, item, kw[item])
            
    def save(_id, account_type, account_value, 'user'):
        
        if getattr(self, '_id', None) == None:
            self._id = collection().insert_one({
                'account_type'  : self.account_type,
                'account_value' : self.account_value,
                'user'          : self.user.toMongoJson()
            }).inserted_id
        else:
            collection().save({
                '_id'           : self._id,
                'account_type'  : self.account_type,
                'account_value' : self.account_value,
                'user'          : self.user.toMongoJson()
            })
        return self    