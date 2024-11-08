# pylint: disable=import-error
from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    # Get the hostname (works both locally and in GKE)
    hostname = socket.gethostname()

    # Try to get the node name from the environment variable (for GKE)
    node_name = os.getenv("NODE_NAME", hostname)  # Fallback to hostname if NODE_NAME is not set

    return f"Hello, Brandee from Flask! Served by node: {node_name}, Hostname: {hostname}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
