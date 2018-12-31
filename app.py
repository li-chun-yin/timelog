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

@app.route('/logout')
def logout():
    from controller import login 
    return login.logout()

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

@app.route('/calendar-tag-remove/<user_tag_id>', methods=['POST'])
def calendar_tag_remove(user_tag_id):
    from controller import calendar
    return calendar.removeTag(user_tag_id)

@app.route('/calendar-events', methods=['GET'])
def calendar_events():
    from controller import calendar
    return calendar.events()

@app.route('/logger-form', methods=['GET'])
@app.route('/logger-form/<user_log_id>', methods=['GET'])
def logger_form(user_log_id=None):
    from controller import logger
    return logger.form(user_log_id)

@app.route('/logger-change-time', methods=['POST'])
def logger_change_time():
    from controller import logger
    return logger.changeTime()

@app.route('/logger-remove', methods=['POST'])
def logger_remove():
    from controller import logger
    return logger.remove()

@app.route('/logger-save', methods=['POST'])
def logger_save():
    from controller import logger
    return logger.save()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
