import hashlib
import random
from datetime import datetime

from src.block import Block


def get_data():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    data = "".join(random.choice(letters) for _ in range(256))
    return data


def get_hash(index: int, prev_hash: str, data: str, nonce: int):
    hashcode = hashlib.sha256(f"{index}{prev_hash}{data}{nonce}".encode('utf-8')).hexdigest()
    return hashcode


def mine(block: Block):
    while block.hashcode[-4] != '0000':
        block.nonce += random.randint(1, 10)
        block.hashcode = get_hash(block.index, block.prev_hash, block.data, block.nonce)
        block.timestamp = datetime.now()
    return block


def block_from_json(block_dict):
    block = Block(
        index=int(block_dict['index']),
        prev_hash=block_dict['prev_hash'],
        hashcode=block_dict['hashcode'],
        data=block_dict['data'],
        nonce=int(block_dict['nonce']),
        timestamp=datetime.strptime(block_dict['timestamp'], '%Y-%m-%d %H:%M:%S.%f'),
        node_id=int(block_dict['node_id'])
    )
    return block
