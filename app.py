#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from lib.datetime import datetime_format

app = Flask(__name__)

app.config.from_pyfile('config.py')
app.jinja_env.filters['date']   = datetime_format
 
@app.route('/', methods=['GET'])
def home():
    from controller import home 
    return home.index()
    
@app.route('/login', methods=['GET'])
def login():
    from controller import login 
    return login.form()

@app.route('/login-email', methods=['POST'])
def login_email():
    from controller import login 
    return login.email()

@app.route('/login-action', methods=['POST'])
def login_action():
    from controller import login 
    return login.action()

@app.route('/calendar', methods=['GET'])
def calendar():
    from controller import calendar
    return calendar.index()

@app.route('/calendar-tag', methods=['GET'])
def calendar_tag():
    from controller import calendar
    return calendar.tag()

@app.route('/calendar-tag-add', methods=['POST'])
def calendar_tag_add():
    from controller import calendar
    return calendar.addTag()

@app.route('/logger-form', methods=['GET'])
@app.route('/logger-form/<user_log_id>', methods=['GET'])
def logger_form(user_log_id=None):
    from controller import logger
    return logger.form(user_log_id)
    
if __name__ == '__main__':
    app.run()
