from flask import Flask
from raft.cluster import Cluster
from timer_thread import TimerThread

app = Flask(__name__)


@app.route('/')
def hello_raft():
    cluster = Cluster()
    return f'raft cluster: {cluster}!'


if __name__ == '__main__':
    timerThread = TimerThread()
    timerThread.start()
    app.run()
