# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

if __name__ == '__main__':
    app.debug = True
    app.run()