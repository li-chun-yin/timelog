# -*- coding: utf-8 -*-

from flask import render_template
from lib import login
from model import UserTag
from flask.globals import request
from excepts.MessageException import MessageException
import json

@login.IfNotLoginThenRedirectToHome
def index():
    #日历页面
    return render_template('calendar/index.html')

@login.IfNotLoginThenRedirectToHome
def tag():
    from lib import tag
    login_user  = login.getUser()
    tag_clors   = tag.colors()
    utc         = UserTag.Client()
    user_tags   = utc.findByUser(login_user['_id'])
    return render_template('calendar/tag.html', user_tags = user_tags, tag_clors = tag_clors)

@login.IfNotLoginThenRedirectToHome
def addTag():
    try:        
        login_user      = login.getUser()
        tag_name        = request.form['tag_name']
        tag_color       = request.form['tag_color']
        utc             = UserTag.Client()
        user_tag_item   = {
            'user_id'   : login_user['_id'],
            'name'      : tag_name,
            'color'     : tag_color
        }
        utc.save(user_tag_item)
        
        # 响应值
        return json.dumps({'status': 'success', 'message' : 'success'})
    except MessageException as e:
        # 响应值
        return json.dumps({'status': 'failed', 'message' : e.value})