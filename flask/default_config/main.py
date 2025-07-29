from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Template rendering example"




if __name__ == '__main__':
    app.run(debug=True, port=5000) # changing the port will require connecting with the hostname ('d78ad65c-flask')