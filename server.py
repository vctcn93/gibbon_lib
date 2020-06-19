from flask import Flask, request
from gibbon.project import Project
import configparser
import os, sys, re

project = None
app = Flask(__name__)


# global project parameter
ORIGIN = [0, 0]


@app.route('/connect')
def connect():
    return """<h1> GIBBON SERVER </h1>
    <p> Now the server is connected, you can calculate your data with cpython. </p>
    """


@app.route('/display')
def display():
    # url= http://127.0.0.1:5000/display?basemap=satellite&poi=null&environment=null
    return ''


def setup():
    pass


def phase_config():
    config = configparser.ConfigParser()
    project = sys.argv[1]
    config_path = f'{project}/config.ini'
    config.read(config_path)
    return config._sections.values()


if __name__ == '__main__':
    setup()
    app.run()
