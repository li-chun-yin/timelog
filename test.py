#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from lib.jinja_extensions import datetime_format

import time
from lib.datetime import datetime_format
t = time.strptime('2018年03月08日 00:00:29','%Y年%m月%d日 %H:%M:%S')
tt = time.mktime(t)
print(datetime_format(tt, '%Y年%m月%d日 %H:%M:%S'))
# print(datetime_format('1545876801', '%Y-%m-%d %H:%M:%S'))

# ac = [{'a':1,'b':2}, {'a':10, 'b':20}]
# 
# for i in ac:
#     print(i['a']) 

# from model import Account
# from random import randrange
# from flask import Flask
# import hashlib
# from datetime import datetime
# from pymongo.mongo_client import MongoClient
# from collections import namedtuple
# import bson
# 
# app = Flask(__name__)
# 
# app.config.from_pyfile('config.py')
# 
# 
# login_name      = str(datetime.now())
# # login_name      = '2018-12-24 18:11:09.918422';
# 
# # 验证码    
# randnum         = str(randrange(1000, 9999))
# 
# # 数据更新
# ac              = Account.Client(MongoClient(app.config['MONGODB_DNS']), 'timelog')
# account         = ac.findByAccountValue(login_name)
# print(account)
# if account:
#     account['user']['user_password']    = hashlib.md5(randnum.encode('utf-8')).hexdigest()
#     account                             = ac.save(account);
# else:
#     account                 = bson.BSON.encode({
#         'account_type'      : '1',
#         'account_value'     : login_name,
#         'user'              : {
#             'user_name'     : '',
#             'user_password' : hashlib.md5(randnum.encode('utf-8')).hexdigest()
#         } 
#     })
#     account                 = bson.BSON.decode(account)
#     
#     for i in account:
#         print (account[i])
    
# 
# #     account                     = namedtuple('account', ['account_type', 'account_value', 'user'])
# #     account.account_type        = '1'
# #     account.account_value       = login_name
# #     account.user                = namedtuple('user', ['user_name', 'user_password'])
# #     account.user.user_name      = '';
# #     account.user.user_password  = hashlib.md5(randnum.encode('utf-8')).hexdigest()
# #     
#     account                     = ac.save(account);
#      
# print(account)
