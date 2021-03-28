from flask import Flask, request, render_template, send_file
import os
import json
from io import BytesIO

try:
    from credentials import CREDENTIALS
except:
    CREDENTIALS = os.environ

import transcript_accessor as trans
import video_summarizer as vid_sum
import docx_generator as docx_gen

app = Flask(__name__)

@app.route('/')
def index():
    return "Main page lecture noted"

#returns text from youtube video, vid is id of youtube video
@app.route('/transcript/<string:vid>')
def transcript(vid):
    return trans.get_transcript(vid)

@app.route('/notes/<string:vid>')
def notes(vid):
    transcript = trans.get_transcript(vid)
    chunks = trans.chunk(transcript)

    data = []
    for chunk in chunks:
        data = data + vid_sum.summarize(chunk)

    for i in range(0, len(data)):
        data[i] = {"type": "text", "data": data[i]}

    print(data)

    return {"response": data}

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
    app.run(debug=True, use_reloader=True)
