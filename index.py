import json, requests, pyotp
from flask import (
    Flask,
    Response,
    request,
    jsonify,
    make_response,
    abort,
    send_from_directory,
)
from flask_cors import CORS
from io import BytesIO
from modules import (
    gettracnghiem,
    lunar,
    color,
    tmp,
    youtube_dl,
    qr,
    morse,
    screenshot,
    dcwebhook,
)

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def home():
    """

    Route to the home page of the web app.

    Returns:
        str: A simple greeting message.

    """
    return "moi?"


@app.route("/tracnghiem/<string:q>", methods=["GET"])
def tracnghiem(q):
    """
    Route to handle the quiz questions and answers.

    Args:
        q (str): The question for which the answer is to be fetched.

    Returns:
        Response: A JSON response containing the answer to the given question.
    """
    output = gettracnghiem.dapan(q)
    json_string = json.dumps(output, ensure_ascii=False)
    return Response(json_string, mimetype="application/json")


@app.route("/lunar", methods=["GET"])
def lunar_convert():
    """
    Route to convert a given Gregorian date to Lunar date.

    Args:
        date (str): The Gregorian date to be converted to Lunar date.

    Returns:
        Response: A JSON response containing the converted Lunar date.
    """
    date = request.args.get("date")
    lular_date = lunar.convert(date)
    return Response(lular_date, mimetype="application/json"), 200


@app.route("/tmp", methods=["GET", "POST"])
def loggertofile():
    """
    Route to log data to a file.

    Args:
        data (str): The data to be logged.
        filename (str): The name of the file to which the data is to be logged.

    Returns:
        Response: A JSON response indicating whether the logging was successful or not.
    """
    if request.method == "GET":
        data = request.args.get("data")
        filename = request.args.get("filename")
    elif request.method == "POST":
        data = request.form.get("data")
        filename = request.form.get("filename")
    try:
        if not data:
            raise ValueError("Data is missing")
        tmp.write(data, filename)
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    return jsonify({"success": True}), 200

    # API trả về hình ảnh tương ứng với mã hex color


@app.route("/color", methods=["GET"])
def getcolor():
    """
    Route to get an image corresponding to a given hex color code.

    Args:
        code (str): The hex color code for which the image is to be generated.
        size (str, optional): The size of the image in the format 'widthxheight'. Defaults to '200x200'.

    Returns:
        Response: A PNG image response corresponding to the given hex color code.
    """
    # Lấy mã màu từ query parameter
    color_value = request.args.get("code")
    print(color_value)
    # Lấy kích thước từ query parameter
    size = request.args.get("size", default="200x200")
    # Chuyển kích thước thành tuple
    size = tuple(map(int, size.split("x")))
    # Kiểm tra nếu mã màu không tồn tại
    if not color_value:
        # Trả về lỗi và thông báo
        response = jsonify({"message": "Missing color parameter"})
        response.status_code = 400
        return response
    try:
        # Trả về hình ảnh từ mã màu
        img_data = color.get_image_from_hex(color_value, size)
        # Trả về hình ảnh
        response = make_response(img_data)
        response.headers.set("Content-Type", "image/png")
        response.headers.set(
            "Content-Disposition", "attachment", filename=color_value + ".png"
        )
        return response
    except Exception as e:
        # Trả về lỗi và thông báo
        response = jsonify({"message": str(e)})
        response.status_code = 500
        return response


@app.route("/screenshot", methods=["GET"])
def get_screenshot():
    """
    Route to take a screenshot of a given URL.

    Args:
        url (str): The URL of the website for which the screenshot is to be taken.

    Returns:
        Response: A PNG image response containing the screenshot of the given URL.
    """
    # Lấy mã màu từ query parameter
    url = request.args.get("url")
    if not url:
        # Trả về lỗi và thông báo
        response = jsonify({"message": "Missing color parameter"})
        response.status_code = 400
        return response
    try:
        # Trả về hình ảnh từ mã màu
        # Trả về hình ảnh
        response = screenshot.take_screenshot(url)
        response.headers.set("Content-Type", "image/png")
        response.headers.set(
            "Content-Disposition", "attachment", filename="screenshot.png"
        )
        return response
    except Exception as e:
        # Trả về lỗi và thông báo
        response = jsonify({"message": str(e)})
        response.status_code = 500
        return response


@app.route("/song", methods=["GET"])
def search_song():
    """
    Route to search for a song on iTunes.

    Args:
        name (str): The name of the song to be searched.

    Returns:
        Response: A JSON response containing the details of the first song that matches the given name.
    """
    song_name = request.args.get("name")
    if not song_name:
        return jsonify({"error": "missing song_name parameter"})
    params = {"term": song_name, "media": "music", "entity": "song", "limit": 1}
    response = requests.get("https://itunes.apple.com/search", params=params)
    if response.status_code != 200:
        return jsonify({"error": "iTunes API returned an error"})
    data = response.json()["results"]
    if not data:
        return jsonify({"error": "song not found"})
    return data[0]


@app.route("/lyrics")
def get_lyrics():
    """
    Route to get the lyrics of a song.

    Args:
        track_name (str): The name of the song for which the lyrics are to be fetched.
        artist_name (str): The name of the artist who sang the song.

    Returns:
        Response: A JSON response containing the lyrics of the given song.
    """
    track_name = request.args.get("track_name")
    artist_name = request.args.get("artist_name")
    if not track_name or not artist_name:
        return jsonify({"error": "missing track_name or artist_name parameter"})
    endpoint = f"https://api.lyrics.ovh/v1/{artist_name}/{track_name}"
    response = requests.get(endpoint)
    if response.status_code != 200:
        return jsonify({"error": "Lyrics.ovh API returned an error"})
    data = response.json()
    if not data["lyrics"]:
        return jsonify({"error": "lyrics not found"})
    return jsonify(
        {"track_name": track_name, "artist_name": artist_name, "lyrics": data["lyrics"]}
    )


@app.route("/qr", methods=["GET"])
def generate_qr():
    """
    Route to generate a QR code for a given data.

    Args:
        data (str): The data for which the QR code is to be generated.
        size (str, optional): The size of the QR code in the format 'widthxheight'. Defaults to '200x200'.

    Returns:
        Response: A PNG image response containing the generated QR code.
    """
    data = request.args.get("data")
    size = request.args.get("size", default="200x200")
    size = tuple(map(int, size.split("x")))
    try:
        img = qr.generate_qr_code(data, size)
    except ValueError as e:
        return Response(str(e), status=400)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return Response(buffer.getvalue(), mimetype="image/png")


@app.route("/en_morse", methods=["GET"])
def encode():
    """
    Route to encode a given text into Morse code.

    Args:
        data (str): The text to be encoded into Morse code.

    Returns:
        Response: A JSON response containing the Morse code for the given text.
    """
    data = request.args.get("data")
    if not data:
        abort(400, "Missing data parameter")
    morse_code = morse.encode(data)
    return jsonify({"morse_code": morse_code})


@app.route("/de_morse", methods=["GET"])
def decode():
    """
    Route to decode a given Morse code into plain text.

    Args:
        data (str): The Morse code to be decoded into plain text.

    Returns:
        Response: A JSON response containing the plain text for the given Morse code.
    """
    data = request.args.get("data")
    if not data:
        abort(400, "Missing data parameter")
    plain_text = morse.decode(data)
    return jsonify({"plain_text": plain_text})


@app.route("/2fa", methods=["GET"])
def totp():
    """
    Route to generate a Time-based One-Time Password (TOTP) for a given secret.

    Args:
        s (str): The secret for which the TOTP is to be generated.
        digits (int, optional): The number of digits in the TOTP. Defaults to 6.
        digest (str, optional): The digest algorithm to be used for the TOTP. Defaults to None.
        name (str, optional): The name of the TOTP. Defaults to None.
        issuer (str, optional): The issuer of the TOTP. Defaults to None.
        interval (int, optional): The interval (in seconds) for which the TOTP is valid. Defaults to 30.

    Returns:
        Response: A JSON response containing the generated TOTP for the given secret.
    """
    s = request.args.get("s")
    digits = int(request.args.get("digits", default=6))
    digest = request.args.get("digest", default=None)
    name = request.args.get("name", default=None)
    issuer = request.args.get("issuer", default=None)
    interval = int(request.args.get("interval", default=30))
    if not s:
        abort(400, "Missing secret parameter")
    code = pyotp.TOTP(s, digits, digest, name, issuer, interval).now()
    return jsonify({"code": code})


@app.route("/ytdl", methods=["GET"])
def download_video():
    """
    Route to download a video or audio from a given URL.

    Args:
        url (str): The URL of the video or audio to be downloaded.
        format (str): The format in which the video or audio is to be downloaded.

    Returns:
        Response: A string response containing the download URL for the given video or audio.
    """
    url = request.args.get("url")
    format = request.args.get("format")
    if not url or not format:
        abort(400, "Missing url or format")
    elif format not in [
        "360",
        "480",
        "720",
        "1080",
        "1440",
        "4k",
        "8k",
        "mp3",
        "m4a",
        "webm",
        "acc",
        "flac",
        "opus",
        "ogg",
        "wav",
    ]:
        abort(
            400,
            f'Invalid format "{format}". \nAvailable formats: \nAUDIO: "mp3, m4a, webm, acc, flac, opus, ogg, wav"; \nVIDEO: "360, 480, 720, 1080, 1440, 4k, 8k"',
        )
    else:
        download_url = youtube_dl.get_download_url(url, format)
        # logger.info(f"")
        return download_url
        return jsonify({"download_url": download_url})


@app.route("/rtmp/<path:filename>", methods=["GET"])
def get_file(filename):
    """
    Route to get a file from the 'files' directory.

    Args:
        filename (str): The name of the file to be fetched.

    Returns:
        Response: A file response containing the requested file from the 'files' directory.
    """
    return send_from_directory("files", filename)


@app.route("/dcwebhook", methods=["POST"])
def sendwebhook():
    """

    Sends a webhook to Discord using the provided ID, token, and data.

    Args:
        id (str): The ID of the Discord webhook.
        token (str): The token of the Discord webhook.
        data (dict): The data to be sent in the webhook.

    Returns:
        Response: The response from the Discord webhook.


    """
    id = request.form.get("id")
    token = request.form.get("token")
    data = request.form.get("data")
    return id + token + data
    Response = dcwebhook.send(id, token, data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
