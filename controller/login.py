# -*- coding: utf-8 -*-

from flask import render_template, request, current_app
from email.mime.text import MIMEText
from random import randrange
from excepts.MessageException import MessageException  
from model import User
import smtplib
import re
import json
from lib import login

def form():
# 登录表单页面
    return render_template('login/form.html')

def email():
# 在登录表单输入email后，发送email登录校验的邮件
    try:
        login_name      = request.form['login_name']
        if not re.search('@', login_name):
            raise MessageException('email格式错误')
        
        # 验证码    
        randnum         = str(randrange(1000, 9999))
        
        # 数据更新
        uc          = User.Client()
        user_item   = uc.findByAccountValue(login_name)
        if user_item:
            user_item['password']   = uc.passwordEncode(randnum)
            uc.save(user_item)
        else:
            user_item           = {
                'name'          : '',
                'password'      : uc.passwordEncode(randnum),
                'accounts'      : [{
                    'type'      : 'email',
                    'value'     : login_name,
                }],
            }
            uc.save(user_item)
                
        # 邮件发送
        msg             = MIMEText('TIMELOG mail 登录验证码:%s' % randnum, r'html', r'utf-8')
        msg['Subject']  = 'TIMELOG MAIL 登录验证码' 
        msg['From']     = current_app.config['SYSTEM_EMAIL_ACCOUNT']
        msg['To']       = login_name
        
        smtp            = smtplib.SMTP(current_app.config['SYSTEM_EMAIL_HOST'])
        smtp.login(current_app.config['SYSTEM_EMAIL_ACCOUNT'], current_app.config['SYSTEM_EMAIL_PASSWORD'])
        smtp.sendmail(current_app.config['SYSTEM_EMAIL_ACCOUNT'], [login_name], msg.as_string())
        smtp.quit()
        
        # 响应值
        return json.dumps({'status': 'success', 'message' : '邮件已发送'})
    except MessageException as e:
        # 响应值
        return json.dumps({'status': 'failed', 'message' : e.value})
        
def action():
    # 登录    
    login_name      = request.form['login_name']
    login_password  = request.form['login_password']
    uc              = User.Client()
    user_item       = uc.findByAccountValue(login_name)
    if uc.loginAble(user_item, login_password):
        
        login.login(user_item)
        return  json.dumps({'status': 'success', 'message' : '登录成功'})
        
    return  json.dumps({'status': 'failed', 'message' : '请检查授权码是否输入正确。'})
