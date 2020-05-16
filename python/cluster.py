import collections

Node = collections.namedtuple('Node', ['id', 'uri'])


class Cluster:
    ids = range(0, 4)
    uris = [f'localhost:500{n}' for n in ids]

    def __init__(self):
        self._nodes = [Node(nid, uri) for nid, uri in enumerate(self.uris, start=0)]

    def __len__(self):
        return len(self._nodes)

    def __getitem__(self, index):
        return self._nodes[index]
