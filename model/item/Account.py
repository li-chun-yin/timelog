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