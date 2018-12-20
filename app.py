#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from controller import home
from controller import calendar
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

app.config.from_pyfile('config.py')

# _connection     = MongoClient(app.config['MONGODB_DNS'])
# _db             = _connection.timelog
# data            = _db.account.find()
# print(_db.account.count());
# print(_db.account.index_information())
# for i in data:
#     print(i)
    
# _db.account2.create_index('account_type', unique=True)
# print(_db.user.index_information())
# print(_db.account2.index_information())

 
app.add_url_rule('/', 'home', home.index)
    
app.add_url_rule('/calendar', 'calendar', calendar.index)
    
if __name__ == '__main__':
    app.debug = True
    app.run()
