import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import subprocess
import json

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"


@app.route("/policecheck/")
@app.route("/policecheck")
def police():
    spz = request.args.get('spz', '')
    # return spz
    import policecheck
    return jsonify(policecheck.check(spz))


@app.route("/upload/", methods=['POST'])
@app.route("/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'erro': 1})
    f = request.files['file']
    if f.filename == '':
        return jsonify({})
    # return jsonify({"name": f.filename})
    filename = '/tmp/' + secure_filename(f.filename)
    f.save(filename)
    return jsonify({"filename": filename})


@app.route("/recognize/")
@app.route("/recognize")
def recognize():
    try:
        filename = request.args.get('filename', '')
        proc = subprocess.Popen(["/usr/bin/alpr", "-c eu", "-n 8", "-j", filename], stdout=subprocess.PIPE)
        output = json.loads(proc.stdout.read().decode("utf-8"))
        return jsonify({'value': 'ok', 'output': output})
    except Exception:
        return jsonify({'value': 'error', 'description': 'No picture found'})


if __name__ == "__main__":
    app.run()
