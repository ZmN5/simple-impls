import socket
import select

import config
from app_params import AppParams
from server import WSGIServer
from scheduler import Scheduler
from scheduler import ReadWait
from scheduler import WriteWait
from scheduler import NewTask


class WSGIServerByCoroutine(WSGIServer):
    def __init__(self, server_address):
        self.sock = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(server_address)
        sock.setblocking(0)
        sock.listen(config.REQUEST_QUEUE_SIZE)
        self.scheduler = Scheduler()

    def loop(self):
        while True:
            yield ReadWait(self.sock)
            client, addr = self.sock.accept()
            print(f'Get a new client {addr}')
            yield NewTask(self.handle_request(client, addr))

    def serve_forever(self):
        self.scheduler.new(self.loop())
        self.scheduler.mainloop()

    def handle_request(self, client, addr):
        yield ReadWait(client)
        request_data = client.recv(1 << 30)
        app_params = AppParams(request_data)
        app_params.parse_request()
        env = app_params.get_environ()
        result = self.application(env, app_params.start_response)
        try:
            status, response_headers = app_params.headers_set
            first_line = f'HTTP/1.1 {status}\r\n'
            headers = '\r\n'.join(
                [f'{header}: {value}' for header, value in response_headers])
            content = '\r\n'.join(result)
            response = ''.join([first_line, headers, '\r\n\r\n', content])
            yield WriteWait(client)
            client.sendall(response.encode())
        finally:
            client.close()
