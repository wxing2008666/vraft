import os
from flask import Flask
from raft.cluster import Cluster
from timer_thread import TimerThread


def start_timer():
    print("start timer")
    timer_thread = TimerThread(int(os.environ.get('NODE_ID')))
    timer_thread.start()


def create_app():
    raft = Flask(__name__)
    start_timer()
    return raft


app = create_app()


@app.route('/')
def hello_raft():
    cluster = Cluster()
    return f'raft cluster: {cluster}!'


if __name__ == '__main__':
    create_app()
    app.run()
