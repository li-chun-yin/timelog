# -*- coding: utf-8 -*-

from flask.globals import session
from flask.helpers import url_for
from flask import redirect
import bson

def login(user):
    # 当用户登录时，将用户数据信息写入到session回话中
    encode_user     = bson.BSON.encode(user)
    session['user'] = encode_user

def logout():
    # 当用户主项时，将用户数据信息从session中移除
    session.pop('user', None)

def getUser():
    encoded_user    = session['user']
    return bson.BSON.decode(encoded_user)  
    
def isLogin():
    # 返回当前客户端是否是登录状态
    return 'user' in session

def IfNotLoginThenRedirectToHome(func):
    # 当用户没有登录时，url调转到主页
    '''
    可以通过python装饰器方法使用，例:
    from lib.login import login
    @IfNotLoginThenRedirectToHome
    def action():
        pass
    '''
    def wrapper(*agrs, **kw):
        if not isLogin():
            redirect(url_for('login'))
        return func(*agrs, **kw)
    return wrapper