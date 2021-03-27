from flask import Flask
import os

try:
    from credentials import CREDENTIALS
except:
    CREDENTIALS = os.environ

import transcript_accessor as trans
import video_summarizer as vid_sum

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

    metadata = trans.get_metadata(vid)

    return {"response": data, "metadata": metadata}

#TODO
#Method to take youtube vid, returns transcript
#Method to summarize transcript to GPT-3
#Method to find words that we want an image associated with it


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
