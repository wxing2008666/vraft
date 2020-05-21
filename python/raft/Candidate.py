import grequests
from NodeState import NodeState
from client import Client
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Candidate(NodeState):
    """ The state of candidate

    The service will become candidate if no heartbeat is heard from leader
    after the election timeout comes.

    Candidate will start a new leader election with current_term+1.
    If the candidate can get quorum votes before the election timeout comes,
    it becomes the leader and send heartbeat to followers immediately.
    Otherwise, start a new election with current_term+1.
    TODO add pre election later
    """

    def __init__(self, node):
        super(Candidate, self).__init__(node)
        self.commitIndex = 0
        self.lastAppliedIndex = 0
        self.votes = []
        self.entries = []
        self.followers = [peer for peer in self.cluster if peer != self.node]
        self.vote_for = self.id  # candidate always votes itself

    def elect(self):
        """ When become to candidate and start to elect:
            1. term + 1
            2. vote itself
            3. send the vote request (VR) to each peer in parallel
            4. return when it is timeout
        """
        self.current_term = self.current_term + 1
        logging.info(f'{self} sends vote request to peers ')
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
