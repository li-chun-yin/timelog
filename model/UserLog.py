# -*- coding: utf-8 -*-

from pymongo import MongoClient
from flask import current_app

class Client(object):
    # 用于处理用户日志数据信息的mongodb操作类
    
    __slots__ = ('_connection', '_db', '_collection')
    
    def __init__(self, connection = None, db = None, collection = None):
        self._connection    = MongoClient(current_app.config['MONGODB_DNS']) if connection == None else connection
        self._db            = self._connection[current_app.config['MONGODB_DATABASE']] if db == None else self._connection[db]
        self._collection    = self._db['user_log'] if collection == None else self._db[collection]
        
    def findById(self, user_log_id):
        #通过id查询用户的日志
        return self._collection.find_one({'_id' : user_log_id })
           
    def save(self, data):
        # 修改用户日志的数据信息
        '''
        为了规范统一数据格式，所以使用这个方法与mongodb交互。
        当data[_id]没有设置的时候会添加新数据
        当data[_id]设置的时候会修改数据
        '''
        user_log                = {
            'user_id'           : data['user_id'],
            'tag_id'            : data['tag_id'],
            'tag_name'          : data['tag_name'],
            'tag_color'         : data['tag_color'],
            'content'           : data['content'],
            'start_time'        : data['start_time'],
            'end_time'          : data['end_time'],
        }
        
        if '_id' in data:
            user_log['_id'] = data['_id']
            
        self._collection.save(user_log)
        
        return user_log
        