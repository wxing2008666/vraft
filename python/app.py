import json
import os
from flask import Flask, jsonify, request
from raft.cluster import Cluster
from timer_thread import TimerThread

NODE_ID = int(os.environ.get('NODE_ID'))
cluster = Cluster()
node = cluster[NODE_ID]
timer_thread = TimerThread(NODE_ID)


def create_app():
    raft = Flask(__name__)
    timer_thread.start()
    return raft


app = create_app()


@app.route('/raft/vote', methods=['POST'])
def request_vote():
    candidate = request.get_json()
    timer_thread.vote(candidate)
    d = {"vote": True, "node": node, "candidate": candidate}
    return jsonify(d)


@app.route('/raft/heartbeat', methods=['POST'])
def heartbeat():
    d = {"alive": True, "node": node}
    return jsonify(d)


@app.route('/')
def hello_raft():
    return f'raft cluster: {cluster}!'


if __name__ == '__main__':
    create_app()
    app.run()
