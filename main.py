import os

import flask
from flask import Flask, render_template, request, Response, make_response
from werkzeug.datastructures import FileStorage
import subprocess

app = Flask(__name__)
PORT = 9999


@app.route("/")
def home():
    return render_template("index.html")


def analyze(file: str):
    filter_command = f"silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-40dB"
    subprocess.run(["ffmpeg", "-hide_banner", "-i", f"./tmp/{file}", "-af", filter_command, f"./tmp/NEW_{file}"])
    os.remove(f"./tmp/{file}")
    f = open(f"./tmp/NEW_{file}", "rb")
    os.remove(f"./tmp/NEW_{file}")
    return f


@app.route("/audio", methods=["POST"])
def audio():
    # audioName = request.form["audio"]
    audioFile: FileStorage = request.files["audio"]
    with open(f"./tmp/{audioFile.filename}", "wb") as f:
        f.write(audioFile.stream.read())

    audioFile.close()
    final = analyze(audioFile.filename)

    return flask.send_file(final, as_attachment=True, download_name=audioFile.filename)


def main():
    app.run(host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
