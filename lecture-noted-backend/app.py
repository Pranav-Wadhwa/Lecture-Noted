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
    transcript = trans.get_transcript(vid)
    # chunks = trans.chunk(transcript)
    chunks, times = trans.get_chunky_transcript(vid)

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

    #print(data)
    #print(transcript)

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

@app.route('/testingv2')
def testing2():
    response= jsonify({ "metadata": { "author": "minutephysics", "dislikes": 601, "duration": "00:01:25", "likes": 18193, "rating": 4.872087, "title": "Minute Physics: What is Gravity?", "viewcount": 2809342 }, "response": [ { "data": "Every object attracts every other object in the universe. The strength of the attraction decreases by the square of the distance between the objects.", "time": "2.95", "type": "text" }, { "data": "The attraction is proportional to the mass of the objects.", "type": "text" }, { "data": "Objects with mass also attract massless particles like light.", "type": "text" }, { "data": { "image": "https://pixabay.com/get/g3bea1aca3179c3747c2468afc8075e72d472a723b90b372e491078f344e88e274eef89e8fad5ea4fe9656d5c93cc55d6526d7037e09b6b2a8df6b8d152fd1835_1280.jpg", "keyword": "objects" }, "type": "image" }, { "data": { "image": "https://pixabay.com/get/gfbe95589d133a725afc3fef40c17bfda673c38a61e320344e96602b5ed6e02c2b8770356eb3ec066025093fc526bfb2b17285e58b79e0334786ce107adf06b62_1280.jpg", "keyword": "attraction" }, "type": "image" }, { "data": { "image": "https://pixabay.com/get/g1660fb43734a0074ea79a2b04cd17dae4eb0d4d7f00861c32960d2875425998ed9fcd5e429d871918ec29a0a116d055723614f4ed3a73ff297d455abc93f7f5e_1280.jpg", "keyword": "light" }, "type": "image" } ] })

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
