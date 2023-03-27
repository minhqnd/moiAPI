from flask import Flask, Response
import gettracnghiem
from threading import Thread
import json


app = Flask(__name__)
from duckduckgo_search import ddg

@app.route('/')
def home():
    return "moi?"

@app.route('/tracnghiem/<string:q>', methods=['GET'])
def tracnghiem(q):
    output = gettracnghiem.dapan(q)
    json_string = json.dumps(output, ensure_ascii=False)
    return Response(json_string, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8080)
