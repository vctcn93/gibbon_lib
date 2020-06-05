from flask import Flask, request
from gibbon.maps import TerrainMap


app = Flask(__name__)


# global project parameter
ORIGIN = [0, 0]


@app.route('/connect')
def connect():
    return """<h1> GIBBON SERVER </h1>
    <p> Now the server is connected, you can calculate your data with cpython. </p>
    """


@app.route('/set_origin')
def set_origin():
    origin = eval(request.args.get('origin'))
    global ORIGIN
    ORIGIN = origin
    return f'Now your project origin changed to {ORIGIN}'


@app.route('/check_project_parameter')
def check_project_parameter():
    return ""


@app.route('/create_terrain')
def create_terrain():
    coords = eval(request.args.get('coords'))
    radius = eval(request.args.get('radius'))
    st = Single

if __name__ == '__main__':
    app.run()
