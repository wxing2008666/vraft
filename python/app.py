from flask import Flask
from raft.cluster import Cluster

app = Flask(__name__)


@app.route('/')
def hello_raft():
    cluster = Cluster()
    return f'raft cluster: {cluster}!'


if __name__ == '__main__':
    app.run()
