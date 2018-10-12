import socket
SERVER_NAME = 'WSGIServer 0.1'
SERVER_HOST = 'localhost'
SERVER_PORT = 8888
SERVER_NAME = socket.getfqdn(SERVER_HOST)
SERVER_TYPE = "coroutine"  # "process"

SERVER = 'coroutine_server.WSGIServerByCoroutine'
# SERVER = 'process_server.WSGIServerByProcess'

REQUEST_QUEUE_SIZE = 1024

URL_SCHEME = 'http'
