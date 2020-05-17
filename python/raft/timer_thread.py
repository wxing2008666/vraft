import sys
from random import randrange
import threading

from Candidate import Candidate
from Follower import Follower
from client import Client
from cluster import Cluster
cluster = Cluster()


class TimerThread(threading.Thread):
    def __init__(self, node_id):
        threading.Thread.__init__(self)
        self.election_timeout = float(randrange(1, 3))
        self.election_timer = threading.Timer(self.election_timeout, self.become_candidate)
        self.node = cluster[node_id]
        self.node_state = Follower(self.node)

    def request_vote(self, peer):
        print(f' {self.node} sent request vote to: {peer} ')
        client = Client()
        with client as session:
            response = session.post(f'http://{peer.uri}/raft/vote', json=self.node)
            print(f'got vote result: {response.status_code}: {response.json()}')

    def become_candidate(self):
        print(f'heartbeat is timeout: {int(self.election_timeout)} s')
        print(f'become candidate and start to request vote ... ')
        self.node_state = Candidate(self.node)
        for peer in cluster:
            if peer != self.node:
                self.request_vote(peer)
                self.node_state.followers.append(Follower(peer))

    def vote(self, candidate):
        print(f' {self.node} got request vote from: {candidate} ')
        result = {"vote": False, "node": self.node, "candidate": candidate}
        if type(self.node_state) == Follower and self.node_state.voteFor is None:
            self.node_state.voteFor = candidate
            result["vote"] = True
            self.become_follower()

        print(f'return vote result: {result} ')
        return result

    def become_follower(self):
        print(f'become follower and reset election timer ... ')
        self.node_state = Follower(self.node)
        self.election_timer.cancel()
        self.election_timer = threading.Timer(float(randrange(1, 3)), self.become_candidate)
        self.election_timer.start()

    def run(self):
        self.become_follower()


if __name__ == '__main__':
    timerThread = TimerThread(int(sys.argv[1]))
    timerThread.start()
