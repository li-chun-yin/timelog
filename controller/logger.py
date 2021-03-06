# -*- coding: utf-8 -*-
from flask.templating import render_template
from flask.globals import request
from lib import login
import time
from model import UserTag, UserLog
from excepts.SystemException import SystemException
from excepts.MessageException import MessageException
import json
from lib.datetime import unixtime, datetime_format

@login.IfNotLoginThenRedirectToHome
def form(user_log_id=None):
    # 日志记录表单
    
    # request params
    user_tag_id     = request.args.get('user_tag', None)
    login_user      = login.getUser()
    
    #moel client
    utc             = UserTag.Client()
    ulc             = UserLog.Client()
    
    #tag options
    tag_options     = utc.findByUser(login_user['_id'])        

    #user log
    nowtime                 = int(time.time())
    now_hour_time           = datetime_format(nowtime, '%Y-%m-%d %H:00:00')
    init_start_time         = unixtime(now_hour_time, '%Y-%m-%d %H:%M:%S')
    init_end_time           = unixtime(now_hour_time, '%Y-%m-%d %H:%M:%S')
    user_log_item           = {
        'user_id'           : login_user['_id'],
        'tag_id'            : '',
        'tag_name'          : '',
        'tag_color'         : '',
        'content'           : '',
        'satisfy'           : 6,
        'start_time'        : init_start_time,
        'end_time'          : init_end_time,
    }
    if user_log_id:
        user_log_item       = ulc.findById(user_log_id)
    user_tag_item   = None
    if user_tag_id:
        user_tag_item       = utc.findById(user_tag_id)
    if user_tag_item:
        user_log_item['tag_id']     = user_tag_item['_id']
        user_log_item['tag_name']   = user_tag_item['name']
        user_log_item['tag_color']  = user_tag_item['color']
    
    if str(user_log_item['user_id']) != str(login_user['_id']):
        raise SystemException('非法操作')
        
    #template
    return render_template('logger/form.html', user_log_item = user_log_item, tag_options = tag_options)

@login.IfNotLoginThenRedirectToHome
def changeTime():
    try:
        login_user                  = login.getUser()
        _id                         = request.form['_id']
        start_ymdhis                = request.form['start_ymdhis']
        end_ymdhis                  = request.form['end_ymdhis']
        
        ulc                         = UserLog.Client()
        user_log_item               = ulc.findById(_id);
        
        if str(user_log_item['user_id']) != str(login_user['_id']):
            raise SystemException('非法操作')
        
        user_log_item['start_time'] = unixtime(start_ymdhis, '%Y-%m-%d %H:%M:%S')
        user_log_item['end_time']   = unixtime(end_ymdhis, '%Y-%m-%d %H:%M:%S')
        ulc.save(user_log_item)
        
        return json.dumps({'status': 'success', 'message' : 'success'})
    except MessageException as e:
        return json.dumps({'status': 'failed', 'message' : e.value})
    except SystemException as e:
        return json.dumps({'status': 'failed', 'message' : '非法操作'})

@login.IfNotLoginThenRedirectToHome
def remove():
    try:        
        login_user      = login.getUser()
        _id             = request.form['_id']
        
        ulc             = UserLog.Client()
        
        user_log_item   = ulc.findById(_id);
        if str(user_log_item['user_id']) != str(login_user['_id']):
            raise SystemException('非法操作')

        ulc.remove(_id)
        
        # 响应值
        return json.dumps({'status': 'success', 'message' : 'success', '_id': str(user_log_item['_id']) })
    except MessageException as e:
        # 响应值
        return json.dumps({'status': 'failed', 'message' : e.value})
    except SystemException as e:
        # 响应值
        return json.dumps({'status': 'failed', 'message' : '非法操作'})

@login.IfNotLoginThenRedirectToHome
def save():
    try:        
        login_user          = login.getUser()
        _id                 = request.form['_id']
        tag_id              = request.form['tag_id']
        tag_name            = request.form['tag_name']
        tag_color           = request.form['tag_color']
        user_log_start_ymd  = request.form['user_log_start_ymd']
        user_log_start_his  = request.form['user_log_start_his']
        user_log_end_ymd    = request.form['user_log_end_ymd']
        user_log_end_his    = request.form['user_log_end_his']
        content             = request.form['content']
        satisfy             = request.form['satisfy']
        
        ulc             = UserLog.Client()

        user_log_item           = {
            '_id'               : _id,
            'user_id'           : login_user['_id'],
            'tag_id'            : tag_id,
            'tag_name'          : tag_name,
            'tag_color'         : tag_color,
            'content'           : content,
            'satisfy'           : int(satisfy) * int(2),
            'start_time'        : unixtime(user_log_start_ymd + ' ' + user_log_start_his, '%Y-%m-%d %H:%M:%S'),
            'end_time'          : unixtime(user_log_end_ymd + ' ' + user_log_end_his, '%Y-%m-%d %H:%M:%S'),
        }
        
        user_log_item           = ulc.save(user_log_item)
        
        # 响应值
        return json.dumps({'status': 'success', 'message' : 'success', '_id': str(user_log_item['_id']) })
    except MessageException as e:
        # 响应值
        return json.dumps({'status': 'failed', 'message' : e.value})
    except SystemException as e:
        # 响应值
        return json.dumps({'status': 'failed', 'message' : '非法操作'})
        

