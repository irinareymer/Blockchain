import json
import time
from datetime import datetime

from src import utils
from src.block import Block


class Node:
    def __init__(self, server_id: int):
        self.id = server_id
        self.chain = []
        self.last_block = None

    def create_genesis(self):
        genesis = Block(
            index=0,
            prev_hash="GENESIS",
            hashcode="hash",
            data="genesis_data",
            nonce=0,
            timestamp=datetime.now(),
            node_id=1
        )
        self.chain.append(genesis)
        self.last_block = genesis
        genesis.print(is_genesis=True)
        return genesis

    def create_new_block(self):
        index = self.last_block.index + 1
        prev_hash = self.last_block.hashcode
        data = utils.get_data()
        nonce = 0
        hashcode = utils.get_hash(index, prev_hash, data, nonce)
        block = Block(
            index=index,
            prev_hash=prev_hash,
            hashcode=hashcode,
            data=data,
            nonce=nonce,
            timestamp=datetime.now(),
            node_id=self.id
        )
        mined_block = utils.mine(block)
        return mined_block

    def handle_received_block(self, received_block):
        json_block = json.loads(received_block)
        block = utils.block_from_json(json_block)
        if block.index == 0:
            self.chain.append(block)
            self.last_block = block
            block.print(is_genesis=True)
            return True
        last_block_index = 0
        if self.last_block is not None:
            last_block_index = self.last_block.index
        if block.index == last_block_index + 1:
            self.chain.append(block)
            self.last_block = block
            block.print()
            return True
        if block.index == last_block_index and block.timestamp < self.last_block.timestamp:
            self.chain[-1] = block
            self.last_block = block
            block.print()
            time.sleep(1)
            return True
        return False

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i-1]
            current_hash = utils.get_hash(
                current_block.index,
                current_block.prev_hash,
                current_block.data,
                current_block.nonce
            )
            if current_block.hashcode != current_hash or prev_block.hashcode != current_block.prev_hash:
                return False
        return True
