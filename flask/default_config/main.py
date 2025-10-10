from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Template rendering example"




if __name__ == '__main__': # 'host' required to be accessible from outside the container - can also be the hostname \/ if you only want it accessible by the HA internal network
    app.run(host="0.0.0.0", port=5000) # changing the port will require connecting with the hostname ('d78ad65c-flask')