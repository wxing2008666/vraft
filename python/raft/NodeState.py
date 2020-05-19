from cluster import Cluster


class NodeState:
    def __init__(self, node=None):
        self.cluster = Cluster()
        self.node = node

        self.id = node.id
        self.current_term = 0

        self.vote_for = None  # node.id of the voted candidate

    # input: candidate (id, current_term, lastLogIndex, lastLogTerm)
    # output: vote_granted (true/false), term (current_term, for candidate to update itself)
    # rule:
    #   1. return false if candidate.term < current_term
    #   2. return true if (voteFor is None or voteFor==candidate.id) and candidate's log is newer than receiver's
    def vote(self, candidate):
        if candidate.current_term < self.current_term:
            return False, self.current_term
        if self.vote_for is None or self.vote_for == candidate.id:
            # TODO check if the candidate's log is newer than receiver's
            return True, self.current_term
        return False
