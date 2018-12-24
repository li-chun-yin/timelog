# -*- coding: utf-8 -*-

from model.client import Client

def collection():
    users = Client.DB['user']
    return users

class Entity(object):
    
    __slots__ = ('id', 'user_name', 'user_password')
     
    def __init__(self, **kw):
        
        for item in kw:
            setattr(self, item, kw[item])

    def toMongoJson(self):
        
        return {
            '_id'           : self._id,
            'user_name'     : self.user_name,
            'user_password' : self.user_password,
        };
        
    def save(self):
        
        if getattr(self, '_id', None) == None:
            self._id                = collection().insert_one({
                'user_name'         : self.user_name,
                'user_password'     : self.user_password
            }).inserted_id
        else:
            collection().save({
                '_id'           : self._id,
                'user_name'     : self.user_name,
                'user_password' : self.user_password
            })
        return self