# -*- coding: utf-8 -*-

from flask import render_template, request, current_app
from email.mime.text import MIMEText
from random import randrange
from exception import MessageException  
import smtplib
import re
import json
import hashlib
from model import Account

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
        randnum         = randrange(1000, 9999)
        
        # 数据更新
        ac              = Account.Client()
        account         = ac.findByAccountValue(login_name)
        if account:
            account.user.user_password   = hashlib.scrypt(randnum)
            account                     = ac.save(account);
        else:
            account                     = object
            account.account_type        = 1
            account.account_value       = login_name
            account.user.user_name      = '';
            account.user.user_password  = hashlib.scrypt(randnum)
            account                     = ac.save(account);
                
        # 邮件发送
        msg             = MIMEText('TIMELOG mail 登录验证码:%s' % randnum, r'html', r'utf-8')
        msg['Subject']  = 'TIMELOG MAIL 登录验证码' 
        msg['From']     = current_app.config['SYSTEM_EMAIL_ACCOUNT']
        msg['To']       = login_name
        
        smtp            = smtplib.SMTP(current_app.config['SYSTEM_EMAIL_HOST'])
        smtp.sendmail(current_app.config['SYSTEM_EMAIL_ACCOUNT'], [login_name], msg)
        smtp.quit()
        
        # 响应值
        return json.encoder({'status': r'success', 'message' : '邮件已发送'})
    except MessageException as e:
        # 响应值
        return json.encoder({'status': r'failed', 'message' : e})
        
def action():
# 登录    
    login_name      = request.form['login_name']
    login_password  = request.form['login_password']
    
    pass
