# -*- coding: utf-8 -*-

from pymongo import MongoClient
from flask import current_app

class Client(object):
    
    CONNECTION  = MongoClient(current_app.config['MONGODB_DNS'])
    DB          = CONNECTION.timelog 
    