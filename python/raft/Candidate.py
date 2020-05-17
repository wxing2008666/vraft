class Candidate:
    def __init__(self, node_id):
        self.id = node_id
        self.term = 0
        self.commitIndex = 0
        self.lastAppliedIndex = 0
        self.followers = []
        self.entries = []
