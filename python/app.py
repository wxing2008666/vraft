from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_raft():
    return 'raft cluster: '


if __name__ == '__main__':
    app.run()
