# -*- coding: utf-8 -*-

from flask import render_template
from lib import login
from model import UserTag, UserLog
from flask.globals import request
from excepts.MessageException import MessageException
import json
from lib.datetime import datetime_format, unixtime
from flask.helpers import url_for

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
    
@login.IfNotLoginThenRedirectToHome
def events():
    events          = []
    login_user      = login.getUser()
    start_ymd       = request.args.get('start')
    end_ymd         = request.args.get('end')    
    ulc             = UserLog.Client()
    user_log_items  = ulc.findUserLogByYmd(login_user['_id'], start_ymd, end_ymd)
    for log in user_log_items:
        events.append({
            'title'             : log['tag_name'],
            'start'             : datetime_format(log['start_time'], '%Y-%m-%d %H:%M:%S'),
            'end'               : datetime_format(log['end_time'], '%Y-%m-%d %H:%M:%S'),
            'backgroundColor'   : log['tag_color'],
            'borderColor'       : log['tag_color'],
            'url'               : url_for('logger_form', user_log_id = str(log['_id']))
        })
    
    return json.dumps(events);
