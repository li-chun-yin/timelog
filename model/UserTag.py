# -*- coding: utf-8 -*-

from pymongo import MongoClient
from flask import current_app
from lib import tag
from excepts.MessageException import MessageException
from excepts.SystemException import SystemException

class Client(object):
    # 用于处理用户标签数据信息的mongodb操作类
    
    __slots__ = ('_connection', '_db', '_collection')
    
    def __init__(self, connection = None, db = None, collection = None):
        self._connection    = MongoClient(current_app.config['MONGODB_DNS']) if connection == None else connection 
        self._db            = self._connection[current_app.config['MONGODB_DATABASE']] if db == None else self._connection[db]
        self._collection    = self._db['user_tag'] if collection == None else self._db[collection]
    
    def findByUser(self, user_id):
        #通过用户id查询该用户管理的日志标签数据
        return self._collection.find({'user_id' : user_id, 'is_delete' : False})
    
    def findById(self, tag_id):
        #通过d查询特定的日志标签数据
        return self._collection.find_one({'_id' : tag_id })
    
    def validate(self, user_tag):
        if len( user_tag['name'] ) == 0:
            raise MessageException('事件标签名字不能为空。')
        if user_tag['color'] not in tag.colors():
            raise SystemException('事件标签配置异常。')
        
    def save(self, data):
        # 修改用户标签的数据信息
        '''
        为了规范统一数据格式，所以使用这个方法与mongodb交互。
        当data[_id]没有设置的时候会添加新数据
        当data[_id]设置的时候会修改数据
        '''
        self.validate(data)
        
        user_tag                = {
            'user_id'           : data['user_id'],
            'name'              : data['name'],
            'color'             : data['color'],
            'is_delete'         : data['is_delete'] if data['is_delete'] else False 
        }
        
        if '_id' in data:
            user_tag['_id'] = user_tag['_id']
            
        self._collection.save(user_tag)
        
        return user_tag
    