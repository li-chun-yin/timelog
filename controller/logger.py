# -*- coding: utf-8 -*-
from flask.templating import render_template
from flask.globals import request
from lib import login
import time
from model import UserTag, UserLog

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
    user_log_item           = {
        'user_id'           : login_user['_id'],
        'tag_id'            : '',
        'tag_name'          : '',
        'tag_color'         : '',
        'content'           : '',
        'start_time'        : int(time.time()),
        'end_time'          : int(time.time()),
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
    
    #template
    return render_template('logger/form.html', user_log_item = user_log_item, tag_options = tag_options)
