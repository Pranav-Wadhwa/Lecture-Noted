from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():

    return "Main page lecture noted"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
