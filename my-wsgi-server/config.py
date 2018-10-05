import socket
SERVER_NAME = 'WSGIServer 0.1'
SERVER_HOST = 'localhost'
SERVER_PORT = 8888
SERVER_NAME = socket.getfqdn(SERVER_HOST)
SERVER_TYPE = "coroutine"  # "process"

REQUEST_QUEUE_SIZE = 10

URL_SCHEME = 'http'
