#!/usr/bin/env python3
import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from flask import Flask, request
from flask_cors import CORS
from model.record import record, read

app = Flask(__name__)
CORS(app)

##### ********* DHT11 ******** ####
@app.route('/Record/', methods=['POST'])
def record_controller():
    return record(request)

@app.route('/Read/<int:id_rp>', methods=['GET'])
def read_controller(id_rp):
    id_sensor = request.args.get('id_sensor', '')
    return read(id_rp, id_sensor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)