import sys
import threading
from random import randrange
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

from Candidate import Candidate
from Follower import Follower
from Leader import Leader
from cluster import Cluster, ELECTION_TIMEOUT_MAX

cluster = Cluster()


class TimerThread(threading.Thread):
    def __init__(self, node_id):
        threading.Thread.__init__(self)
        self.election_timeout = float(randrange(1, 3))
        self.election_timer = threading.Timer(self.election_timeout, self.become_candidate)
        self.node = cluster[node_id]
        self.node_state = Follower(self.node)

    def become_leader(self):
        logging.info(f'become leader and start to send heartbeat ... ')
        self.node_state = Leader(self.node)
        self.node_state.heartbeat()

    def become_candidate(self):
        logging.warning(f'heartbeat is timeout: {int(self.election_timeout)} s')
        logging.info(f'{self.node} become candidate and start to request vote ... ')
        self.node_state = Candidate(self.node)
        self.node_state.elect()
        if self.node_state.win():
            self.become_leader()
        else:
            self.become_follower()

    def vote(self, candidate):
        logging.info(f' {self.node} got request vote from: {candidate} ')
        result = {"vote": False, "node": self.node, "candidate": candidate}
        if type(self.node_state) == Follower and self.node_state.voteFor is None:
            self.node_state.voteFor = candidate
            result["vote"] = True
            self.become_follower()

        logging.info(f'return vote result: {result} ')
        return result

    def become_follower(self):
        timeout = float(randrange(ELECTION_TIMEOUT_MAX / 2, ELECTION_TIMEOUT_MAX))
        if type(self.node_state) != Follower:
            logging.info(f'{self.node} become follower ... ')
            self.node_state = Follower(self.node)
        logging.info(f'follower {self.node} reset election timer {timeout} s ... ')
        self.election_timer.cancel()
        self.election_timer = threading.Timer(timeout, self.become_candidate)
        self.election_timer.start()

    def run(self):
        self.become_follower()


if __name__ == '__main__':
    timerThread = TimerThread(int(sys.argv[1]))
    timerThread.start()
