from datetime import datetime


class LogEntry:
    def __init__(self, index, leader_id, payload):
        self.index = index
        self.term = 0
        self.leaderId = leader_id
        self.payload = payload
        self.creationTime = datetime.utcnow()
