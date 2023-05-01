from threading import Thread
import json
from flask import Flask, Response, request, jsonify, make_response, abort
from flask_cors import CORS
from modules import gettracnghiem, lunar, logger, color, youtube_dl

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


# @app.route('/log', methods=['GET', 'POST'])
# def logger():
#     if request.method == 'GET':
#         data = request.args.get('data')
#         filename = request.args.get('filename')
#     elif request.method == 'POST':
#         data = request.form.get('data')
#         filename = request.form.get('filename')
#     try:
#         if not data:
#             raise ValueError("Data is missing")
#         logger(data, filename)
#     except ValueError as e:
#         return jsonify({'success': False, 'message': str(e)}), 400
#     return jsonify({'success': True}), 200

# API trả về hình ảnh tương ứng với mã hex color
@app.route('/color', methods=['GET'])
def getcolor():
    # Lấy mã hex color từ query parameter
    hex_color = request.args.get('hex')

    # Kiểm tra nếu mã hex color không tồn tại
    if not hex_color:
        # Trả về lỗi và thông báo
        response = jsonify({'message': 'Missing hex color parameter'})
        response.status_code = 400
        return response

    try:
        # Trả về hình ảnh từ mã hex color
        print(hex_color)
        img_data = color.get_image_from_hex(hex_color)

        # Trả về hình ảnh
        response = make_response(img_data)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition', 'attachment', filename='color.png')
        return response
    except Exception as e:
        # Trả về lỗi và thông báo
        response = jsonify({'message': str(e)})
        response.status_code = 500
        return response

@app.route('/ytdl', methods=['GET'])
def download_video():
    url = request.args.get('url')
    format = request.args.get('format')
    if not url or not format:
        abort(400, 'Missing url or format')
    elif format not in ["360", "480", "720", "1080", "1440", "4k", "8k", "mp3", "m4a", "webm", "acc", "flac", "opus", "ogg", "wav"]:
        abort(400, f'Invalid format "{format}". \nAvailable formats: \nAUDIO: "mp3, m4a, webm, acc, flac, opus, ogg, wav"; \nVIDEO: "360, 480, 720, 1080, 1440, 4k, 8k"')
    else:
        download_url = youtube_dl.get_download_url(url, format)
        return jsonify({'download_url': download_url})


if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=8080)
