class Follower:
    def __init__(self, node_id):
        self.id = node_id
        self.leader = None
        self.commitIndex = 0
        self.lastAppliedIndex = 0
        # next log entry to be sent by leader
        self.nextIndex = 0
        # index of highest log entry known to be replicated on server
        self.matchIndex = 0
        self.voteFor = None
        self.entries = []
