from cluster import Cluster


class NodeState:
    def __init__(self, node=None):
        self.node = node
        self.cluster = Cluster()

