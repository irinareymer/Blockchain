import json
import unittest

from src import utils
from src.block import Block
from test.random_data import random_data


class BlockTestCase(unittest.TestCase):
    def test_init_block(self):
        index, prev_hash, hashcode, data, nonce, timestamp, node_id = random_data()
        block = Block(index, prev_hash, hashcode, data, nonce, timestamp, node_id)

        self.assertIsNotNone(block.index)
        self.assertIsNotNone(block.prev_hash)
        self.assertIsNotNone(block.hashcode)
        self.assertIsNotNone(block.data)
        self.assertIsNotNone(block.nonce)
        self.assertIsNotNone(block.timestamp)
        self.assertIsNotNone(block.node_id)

    def test_json(self):
        for i in range(100):
            index, prev_hash, hashcode, data, nonce, timestamp, node_id = random_data()
            block = Block(index, prev_hash, hashcode, data, nonce, timestamp, node_id)
            block_to_json = block.to_json()
            block_from_json = utils.block_from_json(json.loads(block_to_json))

            self.assertEqual(block.index, block_from_json.index)
            self.assertEqual(block.prev_hash, block_from_json.prev_hash)
            self.assertEqual(block.hashcode, block_from_json.hashcode)
            self.assertEqual(block.data, block_from_json.data)
            self.assertEqual(block.nonce, block_from_json.nonce)
            self.assertEqual(block.timestamp, block_from_json.timestamp)
            self.assertEqual(block.node_id, block_from_json.node_id)
