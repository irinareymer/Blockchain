import json
from datetime import datetime


class Block:
    def __init__(
            self,
            index: int,
            prev_hash: str,
            hashcode: str,
            data: str,
            nonce: int,
            timestamp: datetime,
            node_id: int
    ):
        self.index = index,
        self.prev_hash = prev_hash,
        self.hashcode = hashcode,
        self.data = data,
        self.nonce = nonce,
        self.timestamp = timestamp,
        self.node_id = node_id

    def to_json(self):
        block = {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "hashcode": self.hashcode,
            "data": self.data,
            "nonce": self.nonce,
            "timestamp": str(self.timestamp),
            "node_id": self.node_id,
        }
        return json.dumps(block)

    def print(self, is_genesis: bool = False):
        block = f"Block(index={self.index}," \
                f" prev_hash={self.prev_hash}," \
                f" hashcode={self.hashcode}," \
                f" data={self.data}," \
                f" nonce={self.nonce}," \
                f" timestamp={self.timestamp})"
        if is_genesis:
            print(f"Initialized GENESIS: {block}")
        else:
            print(f"Received block from NODE {self.node_id}: {block}")
