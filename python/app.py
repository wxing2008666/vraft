import os
from flask import Flask, request, jsonify
from raft.cluster import Cluster
from timer_thread import TimerThread

NODE_ID = int(os.environ.get('NODE_ID'))
cluster = Cluster()
node = cluster[NODE_ID]


def start_timer():
    print("start timer")
    timer_thread = TimerThread(NODE_ID)
    timer_thread.start()


def create_app():
    raft = Flask(__name__)
    start_timer()
    return raft


app = create_app()


@app.route('/')
def hello_raft():
    return f'raft cluster: {cluster}!'


@app.route('/raft/vote', methods=['POST'])
def request_vote():
    d = {"note": True, "node": node}
    return jsonify(d)


if __name__ == '__main__':
    create_app()
    app.run()
