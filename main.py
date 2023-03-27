from flask import Flask
import gettracnghiem
from threading import Thread


app = Flask(__name__)
from duckduckgo_search import ddg

@app.route('/')
def home():
    return "moi?"

@app.route('/tracnghiem/<string:q>', methods=['GET'])
def tracnghiem(q):
    output = gettracnghiem.dapan(q)
    return output

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8080)