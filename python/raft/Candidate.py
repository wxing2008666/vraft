import grequests
from NodeState import NodeState
from client import Client
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Candidate(NodeState):
    def __init__(self, node):
        super(Candidate, self).__init__(node)
        self.commitIndex = 0
        self.lastAppliedIndex = 0
        self.votes = []
        self.entries = []
        self.followers = [peer for peer in self.cluster if peer != self.node]
        self.vote_for = self.id  # candidate always votes itself

    def elect(self):
        logging.info(f'{self} sends request vote to peers ')
        # vote itself
        self.votes.append(self.node)
        client = Client()
        with client as session:
            posts = [
                grequests.post(f'http://{peer.uri}/raft/vote', json=self.node, session=session)
                for peer in self.followers
            ]
            for response in grequests.imap(posts):
                logging.info(f'{self} got vote result: {response.status_code}: {response.json()}')
                result = response.json()
                if result['vote']:
                    self.votes.append(result['node'])

    def win(self):
        return len(self.votes) > len(self.cluster) / 2

    def __repr__(self):
        return f'{type(self).__name__, self.node.id, self.current_term}'
