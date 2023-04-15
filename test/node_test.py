import unittest
from datetime import datetime

from src import utils
from src.block import Block
from src.node import Node
from test.random_data import random_data


class NodeTestCase(unittest.TestCase):
    def test_init_node(self):
        _, _, _, _, _, _, node_id = random_data()
        node = Node(node_id)

        self.assertIsNotNone(node.id)
        self.assertEqual(node.chain, [])
        self.assertIsNone(node.last_block)

    def test_create_genesis(self):
        _, _, _, _, _, _, node_id = random_data()
        node = Node(node_id)
        genesis = node.create_genesis()

        self.assertEqual(node.id, node_id)
        self.assertEqual(len(node.chain), 1)
        self.assertIsNotNone(node.last_block)
        self.assertEqual(node.last_block, genesis)
        self.assertEqual(node.last_block, node.chain[-1])
        self.assertEqual(node.chain[0].index, 0)
        self.assertEqual(node.chain[0].prev_hash, "GENESIS")
        self.assertEqual(node.chain[0].hashcode, "hash")
        self.assertEqual(node.chain[0].data, "genesis_data")
        self.assertEqual(node.chain[0].nonce, 0)
        self.assertIsNotNone(node.chain[0].timestamp)
        self.assertEqual(node.chain[0].node_id, 1)

    def test_get_data(self):
        for i in range(50):
            self.assertEqual(len(utils.get_data()), 256)

    def test_get_hash(self):
        for i in range(50):
            index, prev_hash, _, data, nonce, _, _ = random_data()
            hashcode = utils.get_hash(index, prev_hash, data, nonce)
            data += "some change"
            new_hashcode = utils.get_hash(index, prev_hash, data, nonce)

            self.assertNotEqual(hashcode, new_hashcode)

    def test_mine(self):
        for i in range(50):
            index, prev_hash, _, data, nonce, timestamp, node_id = random_data()
            hashcode = utils.get_hash(index, prev_hash, data, nonce)
            block = Block(index, prev_hash, hashcode, data, nonce, timestamp, node_id)
            mined_block = utils.mine(block)

            self.assertEqual(mined_block.hashcode[-4:], '0000')

    def test_create_new_block(self):
        _, _, _, _, _, _, node_id = random_data()
        node = Node(node_id)
        node.create_genesis()
        for i in range(50):
            block = node.create_new_block()
            node.chain.append(block)
            node.last_block = block

            self.assertEqual(node.id, node_id)
            self.assertNotEqual(len(node.chain), 0)
            self.assertEqual(node.last_block, block)
            self.assertEqual(node.chain[-1].index, block.index)
            self.assertEqual(node.chain[-1].prev_hash, block.prev_hash)
            self.assertEqual(node.chain[-1].hashcode, block.hashcode)
            self.assertEqual(node.chain[-1].data, block.data)
            self.assertEqual(node.chain[-1].nonce, block.nonce)
            self.assertIsNotNone(node.chain[-1].timestamp)
            self.assertEqual(node.chain[-1].node_id, block.node_id)

    def test_is_chain_valid(self):
        _, _, _, _, _, _, node_id = random_data()
        node = Node(node_id)
        node.create_genesis()
        for i in range(50):
            block = node.create_new_block()
            node.chain.append(block)
            node.last_block = block
            prev_block = node.chain[-2]

            self.assertEqual(prev_block.hashcode == block.prev_hash, node.is_chain_valid())

    def test_handle_received_block(self):
        _, _, _, _, _, _, id_1 = random_data()
        node1 = Node(id_1)
        genesis = node1.create_genesis()
        _, _, _, _, _, _, id_2 = random_data()
        node2 = Node(id_2)
        handle = node2.handle_received_block(genesis.to_json())

        self.assertEqual(len(node2.chain), 1)
        self.assertIsNotNone(node2.last_block)
        self.assertTrue(handle)

        for i in range(50):
            prev_block = node1.chain[-1]
            new_block = node1.create_new_block()
            node1.chain.append(new_block)
            node1.last_block = new_block
            handle = node2.handle_received_block(new_block.to_json())

            self.assertEqual(node2.last_block.index, new_block.index)
            self.assertEqual(node2.last_block.prev_hash, new_block.prev_hash)
            self.assertEqual(node2.last_block.hashcode, new_block.hashcode)
            self.assertEqual(node2.last_block.data, new_block.data)
            self.assertEqual(node2.last_block.nonce, new_block.nonce)
            self.assertEqual(node2.last_block.timestamp, new_block.timestamp)
            self.assertEqual(node2.last_block.node_id, new_block.node_id)
            self.assertEqual(new_block.index == prev_block.index + 1, handle)

        prev_block = node1.chain[-1]
        block = node1.create_new_block()
        block.index = prev_block.index
        block.timestamp = datetime.now().replace(year=1970)
        handle = node2.handle_received_block(block.to_json())

        self.assertEqual(block.timestamp < prev_block.timestamp, handle)
        self.assertEqual(block.index, prev_block.index)
        self.assertEqual(node2.last_block.index, block.index)
        self.assertEqual(node2.last_block.prev_hash, block.prev_hash)
        self.assertEqual(node2.last_block.hashcode, block.hashcode)
        self.assertEqual(node2.last_block.data, block.data)
        self.assertEqual(node2.last_block.nonce, block.nonce)
        self.assertEqual(node2.last_block.timestamp, block.timestamp)
        self.assertEqual(node2.last_block.node_id, block.node_id)
