from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Template rendering example"




if __name__ == '__main__': #   \/ required to be accessible from outside the container
    app.run(debug=True, host="0.0.0.0", port=5000) # changing the port will require connecting with the hostname ('d78ad65c-flask')