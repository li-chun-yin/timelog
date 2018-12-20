#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import render_template

def index():
    return render_template('calendar/index.html')