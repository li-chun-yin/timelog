# -*- coding: utf-8 -*-

from flask import url_for, redirect
from lib import login

def index():
    return redirect(url_for('calendar') if login.isLogin() else url_for('login'))  
