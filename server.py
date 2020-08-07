from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO
from gibbon.project import Project
import configparser
import os, sys, re, json


project = None
app = Flask(__name__)


# global project parameter
DIRECTORY = 'templates/html'


@app.route('/connect')
def connect():
    send_from_directory
    return send_from_directory(DIRECTORY, 'welcome.html')


@app.route('/display')
def display():
    # url= http://127.0.0.1:5000/display?basemap=satellite&poi=null&environment=null
    return ''


if __name__ == '__main__':
    app.run()
