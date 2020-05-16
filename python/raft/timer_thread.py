import sys
from random import randrange
import threading
import time

from cluster import Cluster
cluster = Cluster()


class TimerThread(threading.Thread):
    def __init__(self, node_id):
        threading.Thread.__init__(self)
        self.node = cluster[node_id]
        self.election_timeout = float(randrange(1, 3))

    def request_vote(self, peer):
        print(f' {self.node} request_vote from: {peer} ')

    def become_candidate(self):
        print(f'election_timeout: {int(self.election_timeout)} s')
        print(f'become candidate and start to elect ... ')

        for peer in cluster:
            if peer != self.node:
                self.request_vote(peer)

    def run(self):
        election_timer = threading.Timer(self.election_timeout, self.become_candidate)
        election_timer.start()


if __name__ == '__main__':
    timerThread = TimerThread(int(sys.argv[1]))
    timerThread.start()
