from NodeState import NodeState


class Follower(NodeState):
    def __init__(self, node):
        super(Follower, self).__init__(node)
        self.term = 0
        self.leader = None
        self.commitIndex = 0
        self.lastAppliedIndex = 0
        # next log entry to be sent by leader
        self.nextIndex = 0
        # index of highest log entry known to be replicated on server
        self.matchIndex = 0
        self.voteFor = None
        self.entries = []

    def __repr__(self):
        return f'{type(self).__name__, self.node.id, self.term}'
