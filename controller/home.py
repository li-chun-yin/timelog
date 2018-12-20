#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template
from model.item.Account import Account
from model.item.User import User
from pymongo import errors
from datetime import datetime

def index():
    account_value_prefex = str(datetime.now())
    u = User(user_name='name45', user_password='password45')
    u.save()
    mongo = Account(account_type = 1, account_value = account_value_prefex + 'values', user=u)
#   mongo = Account(account_type = 1, account_value = account_value_prefex + 'values')
    mongo.account_type = '1'
    mongo.account_value = account_value_prefex + 'value'
#     try:
    mongo.save()
#     except errors.DuplicateKeyError as e:
#         return mongo.account_value + str(e)
#         
#     return mongo.account_value
    strv = 'id=' + str( mongo.account_id ) + '&' + str( mongo.account_value ) 
    mongo.account_value = account_value_prefex + 'value2'
    mongo.save()
    strv = strv + 'id=' + str( mongo.account_id ) + '&' + str( mongo.account_value ) 
    mongo.account_value = account_value_prefex + 'value3'
    mongo.save()
    strv = strv + 'id=' + str( mongo.account_id ) + '&' + str( mongo.account_value ) 
    return strv 
    return render_template('home/index.html')
