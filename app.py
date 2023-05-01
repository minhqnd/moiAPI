from threading import Thread
import json
from flask import Flask, Response, request, jsonify, make_response, abort
from flask_cors import CORS
from io import BytesIO
from modules import gettracnghiem, lunar, logger, color, youtube_dl, qr

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
    # Lấy mã màu từ query parameter
    color_value = request.args.get('code')
    print(color_value)
    # Lấy kích thước từ query parameter
    size = request.args.get('size', default='200x200')
    # Chuyển kích thước thành tuple
    size = tuple(map(int, size.split('x')))
    # Kiểm tra nếu mã màu không tồn tại
    if not color_value:
        # Trả về lỗi và thông báo
        response = jsonify({'message': 'Missing color parameter'})
        response.status_code = 400
        return response
    try:
        # Trả về hình ảnh từ mã màu
        img_data = color.get_image_from_hex(color_value, size)
        # Trả về hình ảnh
        response = make_response(img_data)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition',
                             'attachment', filename=color_value+'.png')
        return response
    except Exception as e:
        # Trả về lỗi và thông báo
        response = jsonify({'message': str(e)})
        response.status_code = 500
        return response


@app.route('/qr', methods=['GET'])
def generate_qr():
    data = request.args.get('data')
    size = request.args.get('size', default='200x200')
    size = tuple(map(int, size.split('x')))
    try:
        img = qr.generate_qr_code(data, size)
    except ValueError as e:
        return Response(str(e), status=400)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return Response(buffer.getvalue(), mimetype='image/png')


@app.route('/ytdl', methods=['GET'])
def download_video():
    url = request.args.get('url')
    format = request.args.get('format')
    if not url or not format:
        abort(400, 'Missing url or format')
    elif format not in ["360", "480", "720", "1080", "1440", "4k", "8k", "mp3", "m4a", "webm", "acc", "flac", "opus", "ogg", "wav"]:
        abort(
            400, f'Invalid format "{format}". \nAvailable formats: \nAUDIO: "mp3, m4a, webm, acc, flac, opus, ogg, wav"; \nVIDEO: "360, 480, 720, 1080, 1440, 4k, 8k"')
    else:
        download_url = youtube_dl.get_download_url(url, format)
        # logger.info(f"")
        return jsonify({'download_url': download_url})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
