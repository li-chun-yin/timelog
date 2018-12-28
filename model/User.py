# -*- coding: utf-8 -*-

from pymongo import MongoClient
from flask import current_app
import hashlib
from bson.objectid import ObjectId

class Client(object):
    # 用于处理用户数据信息的mongodb操作类
    
    __slots__ = ('_connection', '_db', '_collection')
    
    def __init__(self, connection = None, db = None, collection = None):
        self._connection    = MongoClient(current_app.config['MONGODB_DNS']) if connection == None else connection 
        self._db            = self._connection[current_app.config['MONGODB_DATABASE']] if db == None else self._connection[db]
        self._collection    = self._db['user'] if collection == None else self._db[collection]
        self._collection.create_index('accounts.value', unique=True);
        
    def passwordEncode(self, password):
        # 密码加密
        return hashlib.md5(password.encode('utf-8')).hexdigest()
        
    def findByAccountValue(self, user_account_value):
        # 通过账号查询一个用户信息
        return self._collection.find_one({'accounts.value' : user_account_value})    
    
    def loginAble(self, user, input_password):
        # 判断user是否可以通过使用输入的密码登录
        '''
        user 用户数据信息
        input_password 通过表单输入的密码
        虽然现在只是判断密码是否输入正确但是考虑以后可能会添加用户状态等判断
        '''
        if user['password'] != self.passwordEncode(input_password):
            
            return False
        
        return True
    
    def save(self, data):
        # 修改用户的数据信息
        '''
        为了规范统一数据格式，所以使用这个方法与mongodb交互。
        当data[_id]没有设置的时候会添加新数据
        当data[_id]设置的时候会修改数据
        '''
        user                    = {
            'name'              : data['name'],
            'password'          : data['password'],
            'accounts'          : []
        }
        
        for account in data['accounts']:
            user['accounts'].append({
                'type'          : account['type'],
                'value'         : account['value'] 
            })
        
        if '_id' in data:
            user['_id'] = ObjectId(data['_id'])
            
        self._collection.save(user)
        
        return user
        