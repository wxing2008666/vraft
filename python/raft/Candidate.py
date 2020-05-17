from NodeState import NodeState


class Candidate(NodeState):
    def __init__(self, node):
        super(Candidate, self).__init__(node)
        self.term = 0
        self.commitIndex = 0
        self.lastAppliedIndex = 0
        self.followers = []
        self.entries = []
