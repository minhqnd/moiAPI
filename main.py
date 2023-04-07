from threading import Thread
import json
from flask import Flask, Response, request
from flask_cors import CORS
import gettracnghiem
import lunar

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def home():
    return "moi?"

@app.route('/tracnghiem/<string:q>', methods=['GET'])
def tracnghiem(q):
    output = gettracnghiem.dapan(q)
    json_string = json.dumps(output, ensure_ascii=False)
    return Response(json_string, mimetype='application/json')

@app.route('/lunar', methods=['GET'])
def lunar_convert():
    date = request.args.get('date')
    print('hellooooo')
    lular_date = lunar.convert(date)
    return Response(lular_date, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=False)
    # app.run(debug=True,host='0.0.0.0',port=8080)
