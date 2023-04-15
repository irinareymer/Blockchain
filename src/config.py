import os

SERVER_ID = int(os.environ.get("SERVER_ID", 1))
SERVER_HOST = os.environ.get("SERVER_HOST", "localhost")
SERVER_PORT = int(os.environ.get("SERVER_PORT", 8001))

FIRST_PORT = int(os.environ.get("FIRST_PORT", 8001))
SECOND_PORT = int(os.environ.get("SECOND_PORT", 8002))
THIRD_PORT = int(os.environ.get("THIRD_PORT", 8003))
