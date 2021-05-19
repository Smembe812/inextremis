from __future__ import print_function
import os
import json
# import sounddevice as sd
# import soundfile as sf
# import pathlib
# import audioread
from pydub import AudioSegment
from pydub.playback import play
from flask import Flask, jsonify, Response, stream_with_context, request, send_file
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from wsgiref.util import FileWrapper
import requests
import io
import json
import uuid
from tinytag import TinyTag
import eyed3
import urllib
import validators

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

relative_path='/assets/song.mp3'

class Audio(object):
    def __init__(self, re_path):
        self.path=None
        if validators.url(re_path):
            self.path = re_path
            self.isUrl = True
        else:
            self.path = os.getcwd() + re_path
            self.isUrl = False
        self.set_buffer(self.path)
        self.set_read_stream(self.buffer)
    def set_buffer(self, path):
        if self.isUrl:
            data = urllib.request.urlopen(path).read()
            self.buffer=io.BytesIO(data)
        else:
            data = open(path, 'rb').read()
            self.buffer=io.BytesIO(data)
        return self
    def set_read_stream(self, buffer):
        self.read_stream=FileWrapper(buffer)
        return self
    
songs_fra_source = [
    {
        "url": "https://assets.mixkit.co/music/preview/mixkit-hazy-after-hours-132.mp3",
        "artist": " Alejandro Magaña (A. M.)",
        "title": "Hazy After Hours"
    },
    {
        "url": "https://assets.mixkit.co/music/preview/mixkit-sleepy-cat-135.mp3",
        "artist": "Alejandro Magaña (A. M.)",
        "title": "Sleepy Cat"
    },
    {
        "url": "https://assets.mixkit.co/music/preview/mixkit-tech-house-vibes-130.mp3",
        "artist": "Alejandro Magaña (A. M.)",
        "title": "Tech House vibes"
    }
]

def make_songs_resource(song):
    uuid4=str(uuid.uuid4())
    song = {
        **song,
        "uuid":uuid4,
        "proxy_url":"/songs/"+uuid4+"/play",
        "art_work":["/img/770x764/8-bit-scream.jpg", "/img/150x150/8-bit-scream.jpg"]
    }
    return song

music=list(map(make_songs_resource, songs_fra_source))

def main():
    song = Audio("https://assets.mixkit.co/music/preview/mixkit-sleepy-cat-135.mp3")
    dance = AudioSegment.from_file(song.buffer, format="mp3")
    play(dance)

# Mostly a test this one    
@socketio.on("my song")
def play_my_song():
    # socketio.emit('my song', {'data': 42})
    emit('my song', Response(song.read_stream, mimetype="audio/mpeg3", direct_passthrough=True), broadcast=True)

@app.route("/")
def hello():
    song = Audio(music[2]['url'])
    return Response(song.read_stream, mimetype="audio/mpeg3", direct_passthrough=True)

@app.route('/songs')
def songs():
    return jsonify(music)

@app.route('/songs/<id>/play')
def play_song(id):
    s=list(filter(lambda song: str(song["uuid"]) == id, music))
    tp=Audio(s[0]["url"])
    response=Response(tp.read_stream, mimetype="audio/mpeg3", direct_passthrough=True)
    response.headers["x-suggested-filename"] = s[0]["title"]+'.mp3'
    response.headers["Content-Disposition"] = "attachment; filename="+s[0]["title"]+'.mp3'
    return response

@app.route('/img/<resolution>/8-bit-scream.jpg')
def album_art(resolution="770x764"):
    img_src="https://madeinshoreditch.co.uk/wp-content/uploads/2016/03/lister-2-1-"+resolution+".jpg"
    data = urllib.request.urlopen(img_src).read()
    img_io=io.BytesIO(data)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg', attachment_filename=""+resolution+"-8-bit-scream.jpg" ,as_attachment=True)

if __name__ == "__main__":
    main()