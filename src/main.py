import threading
import time

from src import utils
from src.config import SERVER_ID, SERVER_HOST, SERVER_PORT, FIRST_PORT, SECOND_PORT, THIRD_PORT
from src.node import Node
from flask import Flask, request
import grequests
from gevent import monkey
import logging


monkey.patch_all()
logging.getLogger('werkzeug').disabled = True


class Server:
    def __init__(self, server_id, server_port):
        self.id = server_id
        self.host = SERVER_HOST
        self.port = server_port
        self.peer_ports = self.peer_ports_dict[self.port]
        self.node = Node(self.id)
        self.received = False
        self.stop = False

    peer_ports_dict = {
        FIRST_PORT: [SECOND_PORT, THIRD_PORT],
        SECOND_PORT: [FIRST_PORT, THIRD_PORT],
        THIRD_PORT: [FIRST_PORT, SECOND_PORT],
    }

    def start(self):
        app = Flask(__name__)

        peer_urls = [
            utils.make_url(self.host, self.peer_ports[0]),
            utils.make_url(self.host, self.peer_ports[1])
        ]

        def generate_new_block():
            while not self.stop:
                if self.id == 1 and len(self.node.chain) == 0:
                    genesis_block = self.node.create_genesis()
                    self.broadcast_block(genesis_block, peer_urls)
                if len(self.node.chain) != 0:
                    new_block = self.node.create_new_block()
                    if not self.received:
                        self.node.chain.append(new_block)
                        self.node.last_block = new_block
                        self.broadcast_block(new_block, peer_urls)
                time.sleep(1)

        @app.route("/", methods=['POST'])
        def server_handler():
            received_block = request.get_json()
            self.received = True
            try:
                self.node.handle_received_block(received_block)
                time.sleep(1)
                self.received = False
                return "Received new block"
            except BaseException as e:
                print(f"Exception: {e}")
                self.received = False
                return "Error"

        unit = threading.Thread(target=app.run, args=(self.host, self.port))
        unit.daemon = True
        generator = threading.Thread(target=generate_new_block)
        unit.start()
        generator.start()
        time.sleep(1)

    def broadcast_block(self, block, peer_urls):
        if not self.received:
            req = (grequests.post(url, json=block.to_json()) for url in peer_urls)
            grequests.map(req)

    def stop_thread(self):
        self.stop = True


if __name__ == '__main__':
    server = Server(SERVER_ID, SERVER_PORT)
    server.start()
