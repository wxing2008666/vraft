from Follower import Follower
from NodeState import NodeState
from client import Client


class Candidate(NodeState):
    def __init__(self, node):
        super(Candidate, self).__init__(node)
        self.term = 0
        self.commitIndex = 0
        self.lastAppliedIndex = 0
        self.votes = []
        self.entries = []
        self.followers = [peer for peer in self.cluster if peer != self.node]

    def request_vote(self, peer):
        print(f' {self.node} sent request vote to: {peer} ')
        client = Client()
        with client as session:
            response = session.post(f'http://{peer.uri}/raft/vote', json=self.node)
            print(f'got vote result: {response.status_code}: {response.json()}')
            return response.json()

    def elect(self):
        for peer in self.followers:
            response = self.request_vote(peer)
            if response['vote']:
                self.votes.append(Follower(peer))

    def win(self):
        return len(self.votes) > len(self.cluster)/2
