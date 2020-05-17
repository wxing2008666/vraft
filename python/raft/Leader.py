from NodeState import NodeState


class Leader(NodeState):
    def __init__(self, node):
        super(Leader, self).__init__(node)
        self.term = 0
        self.commitIndex = 0
        self.lastAppliedIndex = 0
        self.entries = []
        self.followers = [peer for peer in self.cluster if peer != self.node]

    def _heartbeat(self, peer):
        print(f'leader ({self.node}) send heartbeat to peer: {peer}')

    def heartbeat(self):
        for peer in self.followers:
            self._heartbeat(peer)
