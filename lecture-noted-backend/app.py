from flask import Flask, jsonify, request, send_file
import os
import urllib
import json
from io import BytesIO

try:
    from credentials import CREDENTIALS
except:
    CREDENTIALS = os.environ

import transcript_accessor as trans
import video_summarizer as vid_sum
import docx_generator as docx_gen
import keyword_finder as kf

app = Flask(__name__)

@app.route('/')
def index():
    return "Main page lecture noted"

#returns text from youtube video, vid is id of youtube video
@app.route('/transcript/<string:vid>')
def transcript(vid):
    response = jsonify(trans.get_transcript(vid))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/mp3notes/')
def mp3notes():
    rawurl = request.query_string.decode().split("?")[0].split("=")[1]
    extension = request.query_string.decode().split("?")[-1]
    #print(rawurl)
    loc = urllib.parse.unquote_plus(rawurl)
    #print("we made it")
    #print(loc)
    #print(loc.split("/")[-1].split("?")[0])

    transcript = trans.get_mp3_transcript(rawurl+"?"+extension, loc.split("/")[-1].split("?")[0] + ".wav")
    chunks = trans.chunk(transcript)
    #print("we vibin")
    #print(chunks)

    data = []
    for chunk in chunks:
        data = data + vid_sum.summarize(chunk)


    for i in range(0, len(data)):
        data[i] = {"type": "text", "data": data[i]}

    data = data + [{"type": "image", "data": item} for item in kf.get_images(transcript)]

    response = jsonify({"response": data, "metadata": {"filename": rawurl+"?"+extension}})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/notes/<string:vid>')
def notes(vid):
    # transcript = trans.get_transcript(vid)
    # chunks = trans.chunk(transcript)
    chunks, times = get_chunky_transcript(vid)

    data = []
    for i in range(len(chunks)):
        bullets = vid_sum.summarize(chunks[i])

        #    idk if we want to do this
        # if len(bullets) == 1:
        #     bullets = vid_sum.summarize(chunks[i])

        data.append({'type': 'text', 'data': bullets[0], 'time': times[i]})
        for bullet in bullets[1:]:
            data.append({'type': 'text', 'data': bullet})

    # data = []
    # for chunk in chunks:
    #     data = data + vid_sum.summarize(chunk)

    # for i in range(0, len(data)):
    #     data[i] = {"type": "text", "data": data[i]}

    data = data + [{"type": "image", "data": item} for item in kf.get_images(transcript)]

    metadata = trans.get_metadata(vid)

    response = jsonify({"response": data, "metadata": metadata})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/testing')
def testing():
    response = jsonify({"metadata":{"author":"minutephysics","dislikes":601,"duration":"00:01:25","likes":18193,"rating":4.872087,"title":"Minute Physics: What is Gravity?","viewcount":2809263},"response":[{"data":"Gravity is a long range attractive force between all objects with mass.","type":"text"},{"data":"Every massive object attracts every other in the universe.","type":"text"},{"data":"The strength of gravity decreases by the square of the distance between two objects \u2013 so if you're twice as far away, gravity is only one fourth as strong!","type":"text"}]})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/docx')
def generate_doc():
    data = json.loads(request.args.get('data'))
    document = docx_gen.get_document(data)
    fs = BytesIO()
    document.save(fs)
    fs.seek(0)
    return send_file(fs, as_attachment=True, attachment_filename="notes.docx")

#TODO
#Method to take youtube vid, returns transcript
#Method to summarize transcript to GPT-3
#Method to find words that we want an image associated with it


if __name__ == '__main__':
    #url = "https://firebasestorage.googleapis.com/v0/b/lecture-noted.appspot.com/o/2-Minute%20Neuroscience%20-%20Stages%20of%20Sleep.wav?alt=media&token=01ee91db-114d-4892-849a-aa5248f3c050"
    #print(trans.get_mp3_transcript(url, "sleep.mp3"))
    app.run(debug=True, use_reloader=True)
