from threading import Thread
import json, requests, pyotp
from flask import Flask, Response, request, jsonify, make_response, abort, send_from_directory
from flask_cors import CORS
from io import BytesIO
from bs4 import BeautifulSoup
from modules import gettracnghiem, lunar, logger, color, youtube_dl, qr, morse, screenshot

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
    
@app.route('/screenshot', methods=['GET'])
def get_screenshot():
    # Lấy mã màu từ query parameter
    url = request.args.get('url')
    if not url:
        # Trả về lỗi và thông báo
        response = jsonify({'message': 'Missing color parameter'})
        response.status_code = 400
        return response
    try:
        # Trả về hình ảnh từ mã màu
        # Trả về hình ảnh
        response = screenshot.take_screenshot(url)
        response.headers.set('Content-Type', 'image/png')
        response.headers.set('Content-Disposition',
                             'attachment', filename='screenshot.png')
        return response
    except Exception as e:
        # Trả về lỗi và thông báo
        response = jsonify({'message': str(e)})
        response.status_code = 500
        return response


@app.route('/song', methods=['GET'])
def search_song():
    song_name = request.args.get('name')
    if not song_name:
        return jsonify({'error': 'missing song_name parameter'})
    params = {
        'term': song_name,
        'media': 'music',
        'entity': 'song',
        'limit': 1
    }
    response = requests.get('https://itunes.apple.com/search', params=params)
    if response.status_code != 200:
        return jsonify({'error': 'iTunes API returned an error'})
    data = response.json()['results']
    if not data:
        return jsonify({'error': 'song not found'})
    return data[0]

@app.route('/lyrics')
def get_lyrics():
    track_name = request.args.get('track_name')
    artist_name = request.args.get('artist_name')
    if not track_name or not artist_name:
        return jsonify({'error': 'missing track_name or artist_name parameter'})
    endpoint = f'https://api.lyrics.ovh/v1/{artist_name}/{track_name}'
    response = requests.get(endpoint)
    if response.status_code != 200:
        return jsonify({'error': 'Lyrics.ovh API returned an error'})
    data = response.json()
    if not data['lyrics']:
        return jsonify({'error': 'lyrics not found'})
    return jsonify({
        'track_name': track_name,
        'artist_name': artist_name,
        'lyrics': data['lyrics']
    })

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


@app.route('/en_morse', methods=['GET'])
def encode():
    data = request.args.get('data')
    if not data:
        abort(400, 'Missing data parameter')
    morse_code = morse.encode(data)
    return jsonify({'morse_code': morse_code})


@app.route('/de_morse', methods=['GET'])
def decode():
    data = request.args.get('data')
    if not data:
        abort(400, 'Missing data parameter')
    plain_text = morse.decode(data)
    return jsonify({'plain_text': plain_text})


@app.route('/2fa', methods=['GET'])
def totp():
    s = request.args.get('s')
    digits = int(request.args.get('digits', default=6))
    digest = request.args.get('digest', default=None)
    name = request.args.get('name', default=None)
    issuer = request.args.get('issuer', default=None)
    interval = int(request.args.get('interval', default=30))
    if not s:
        abort(400, 'Missing secret parameter')
    code = pyotp.TOTP(s, digits, digest, name, issuer, interval).now()
    return jsonify({'code': code})


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

@app.route('/files/<path:filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory('files', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
