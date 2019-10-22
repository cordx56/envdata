#!/usr/bin/env python3

import os
import time
import glob
from flask import Flask, request, jsonify
from utils.envdataio import EnvdataBin

app = Flask(__name__)

filesRoot = '/data'

@app.route('/v1/info')
def getInfo():
    filelist = glob.glob(os.path.join(filesRoot, '*.bin'))
    return jsonify({
        'status': True,
        'files': [os.path.basename(x) for x in filelist],
        'timezone': ''
    })

@app.route('/v1/now')
def getNowData():
    filename = request.args.get('filename')
    filename = 'envdata.bin' if filename is None else filename
    filename = os.path.join(filesRoot, filename)
    if not os.path.isfile(filename):
        return jsonify({ 'status': False, 'message': "File not found" }), 404
    try:
        with EnvdataBin(filename) as f:
            d = f.read(-1)
            return jsonify({ 'status': True, 'data': [ d.getDict() ] })
    except Exception as e:
        print(e)
        return jsonify({ 'status': False, 'message': str(e) }), 500

@app.route('/v1/data/<filename>/latest')
def getLatestData(filename='envdata.bin'):
    filename = os.path.join(filesRoot, filename)
    if not os.path.isfile(filename):
        return jsonify({ 'status': False, 'message': "File not found" }), 404
    hours = request.args.get('hours')
    try:
        hours = 6.0 if hours is None else float(hours)
    except Exception as e:
        return jsonify({ 'status': False, 'message': str(e) }), 400
    try:
        with EnvdataBin(filename) as f:
            d = [d.getDict() for d in f.readTsRange(None if hours == 0.0 else time.time() - hours * 3600, None)]
            return jsonify({ 'status': True, 'data': d })
    except Exception as e:
        print(e)
        return jsonify({ 'status': False, 'message': str(e) }), 500

if __name__ == "__main__":
    port = 5000
    app.run(host = "0.0.0.0", port = port)
