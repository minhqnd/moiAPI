from threading import Thread
import json
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from modules import gettracnghiem, lunar, logger

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
    lular_date = lunar.convert(date)
    return Response(lular_date, mimetype='application/json'), 200


@app.route('/log', methods=['GET', 'POST'])
def logger():
    if request.method == 'GET':
        data = request.args.get('data')
        filename = request.args.get('filename')
    elif request.method == 'POST':
        data = request.form.get('data')
        filename = request.form.get('filename')
    try:
        if not data:
            raise ValueError("Data is missing")
        logger(data, filename)
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    return jsonify({'success': True}), 200


if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=8080)
