import random
from datetime import datetime

from src import utils


def random_data():
    index = random.randint(1, 100)
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    prev_hash = "".join(random.choice(letters) for _ in range(16))
    data = utils.get_data()
    nonce = random.randint(1, 100)
    hashcode = utils.get_hash(index, prev_hash, data, nonce)
    timestamp = datetime.now()
    node_id = random.randint(1, 3)
    return index, prev_hash, hashcode, data, nonce, timestamp, node_id
