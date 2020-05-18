import collections

Node = collections.namedtuple('Node', ['id', 'uri'])
CLUSTER_SIZE = 5
ELECTION_TIMEOUT_MAX = 10
HEART_BEAT_INTERVAL = float(ELECTION_TIMEOUT_MAX/5)


class Cluster:
    ids = range(0, CLUSTER_SIZE)
    uris = [f'localhost:500{n}' for n in ids]

    def __init__(self):
        self._nodes = [Node(nid, uri) for nid, uri in enumerate(self.uris, start=0)]

    def __len__(self):
        return len(self._nodes)

    def __getitem__(self, index):
        return self._nodes[index]

    def __repr__(self):
        return ", ".join([f'{n.id}@{n.uri}' for n in self._nodes])


if __name__ == '__main__':
    cluster = Cluster()
    print(cluster)
