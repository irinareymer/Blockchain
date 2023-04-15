import time
import unittest

from src.main import Server
from src.config import SERVER_ID, SERVER_PORT


class ServerTestCase(unittest.TestCase):

    def test_init_server(self):
        server = Server(SERVER_ID, SERVER_PORT)

        self.assertIsNotNone(server.id)
        self.assertIsNotNone(server.host)
        self.assertIsNotNone(server.port)
        self.assertIsNotNone(server.peer_ports)
        self.assertIsNotNone(server.node)
        self.assertIsNotNone(server.received)
        self.assertIsNotNone(server.stop)

    def test_start_server(self):
        server3 = Server(3, 8003)
        server2 = Server(2, 8002)
        server1 = Server(1, 8001)

        server3.start()
        server2.start()
        server1.start()

        while len(server3.node.chain) < 20 or len(server2.node.chain) < 20:
            time.sleep(1)

        self.assertEqual(server1.node.chain[0].to_json(), server2.node.chain[0].to_json())
        self.assertEqual(server2.node.chain[0].to_json(), server3.node.chain[0].to_json())
        self.assertEqual(server3.node.chain[0].to_json(), server1.node.chain[0].to_json())

        self.assertTrue(server1.node.is_chain_valid())
        self.assertTrue(server2.node.is_chain_valid())
        self.assertTrue(server3.node.is_chain_valid())

        server3.stop_thread()
        server2.stop_thread()
        server1.stop_thread()
