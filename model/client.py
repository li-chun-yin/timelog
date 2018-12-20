#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient

class Client(object):
    
    def getConnection(self):
        return MongoClient('mongodb://localhost:27017/');
    