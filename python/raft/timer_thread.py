import sys
import threading
from random import randrange
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

from Candidate import Candidate, VoteRequest
from Follower import Follower
from Leader import Leader
from cluster import Cluster, ELECTION_TIMEOUT_MAX

cluster = Cluster()


class TimerThread(threading.Thread):
    def __init__(self, node_id):
        threading.Thread.__init__(self)
        self.node = cluster[node_id]
        self.node_state = Follower(self.node)
        self.election_timeout = float(randrange(ELECTION_TIMEOUT_MAX / 2, ELECTION_TIMEOUT_MAX))
        self.election_timer = threading.Timer(self.election_timeout, self.become_candidate)

    def become_leader(self):
        logging.info(f'{self} become leader and start to send heartbeat ... ')
        self.node_state = Leader(self.node_state)
        self.node_state.heartbeat()

    def become_candidate(self):
        logging.warning(f'heartbeat is timeout: {int(self.election_timeout)} s')
        logging.info(f'{self} become candidate and start to request vote ... ')
        self.node_state = Candidate(self.node_state)
        self.node_state.elect()
        if self.node_state.win():
            self.become_leader()
        else:
            self.become_follower()

    # input: candidate (id, term, lastLogIndex, lastLogTerm)
    # output: term, vote_granted
    # rule:
    #   1. return false if candidate.term < current_term
    #   2. return true if (voteFor is None or voteFor==candidate.id) and candidate's log is newer than receiver's
    def vote(self, vote_request: VoteRequest):
        logging.info(f'{self} got vote request: {vote_request} ')
        vote_result = self.node_state.vote(vote_request)
        if vote_result[0]:
            self.become_follower()
        logging.info(f'{self} return vote result: {vote_result} ')
        return vote_result

    def become_follower(self):
        timeout = float(randrange(ELECTION_TIMEOUT_MAX / 2, ELECTION_TIMEOUT_MAX))
        if type(self.node_state) != Follower:
            logging.info(f'{self} become follower ... ')
            self.node_state = Follower(self.node)
        logging.info(f'{self} reset election timer {timeout} s ... ')
        self.election_timer.cancel()
        self.election_timer = threading.Timer(timeout, self.become_candidate)
        self.election_timer.start()

    def run(self):
        self.become_follower()

    def __repr__(self):
        return f'{type(self).__name__, self.node_state}'


if __name__ == '__main__':
    timerThread = TimerThread(int(sys.argv[1]))
    timerThread.start()
