from flask import Flask
import os

try:
    from credentials import CREDENTIALS
except:
    CREDENTIALS = os.environ

app = Flask(__name__)

@app.route('/')
def index():
    return "Main page lecture noted"

#returns text from youtube video
@app.route('/process/<string:vid>')
def video():
    return "text"

#TODO
#Method to take youtube vid, returns transcript
#Method to summarize transcript to GPT-3
#Method to find words that we want an image associated with it


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
