This is a Flask web app that provides a variety of useful APIs.

The APIs include:

* A quiz question and answer API
* A Lunar date converter API
* A logger to file API
* A color image generator API
* A screenshot API
* A song search API
* A lyrics API
* A QR code generator API
* A Morse code encoder and decoder API
* A Time-based One-Time Password (TOTP) generator API
* A video and audio download API
* A file download API
* A Discord webhook sender API

To run the app, simply install the dependencies and run the following command:

```
python app.py
```

The app will be running on port 8080. You can access the APIs by sending HTTP requests to the appropriate endpoints. For example, to get the answer to a quiz question, you would send a GET request to the following endpoint:

```
http://localhost:8080/tracnghiem/<question>
```

Where `<question>` is the text of the quiz question.

The app also includes a logging system that logs all requests and responses to the console. This can be useful for debugging purposes.