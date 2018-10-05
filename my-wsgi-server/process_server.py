import os
import socket
import signal

from app_params import AppParams
from server import WSGIServer
import config


def grim_reaper(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
        except OSError:
            return

        if pid == 0:
            return


class WSGIServerByProcess(WSGIServer):
    def __init__(self, server_address):
        self.sock = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(server_address)
        sock.listen(config.REQUEST_QUEUE_SIZE)

    def serve_forever(self):
        while True:
            try:
                self.client_connection, _ = self.sock.accept()
            except IOError as e:
                code, _ = e.args
                if code == errno.EINTR:
                    continue
                else:
                    raise e
            self.handle_request()

    def handle_request(self):
        pid = os.fork()
        if pid == 0:
            self.sock.close()
            self.handle_per_request()
            os._exit(0)
        else:
            self.client_connection.close()

    def handle_per_request(self):
        request_data = self.client_connection.recv(1 << 30)
        app_params = AppParams(request_data)
        app_params.parse_request()
        env = app_params.get_environ()
        result = self.application(env, app_params.start_response)
        self.finish_response(app_params, result)

    def finish_response(self, app_params, result):
        try:
            status, response_headers = app_params.headers_set
            first_line = f'HTTP/1.1 {status}\r\n'
            headers = '\r\n'.join(
                [f'{header}: {value}' for header, value in response_headers])
            content = '\r\n'.join(result)
            response = ''.join([first_line, headers, '\r\n\r\n', content])
            self.client_connection.sendall(response.encode())
        finally:
            self.client_connection.close()

    @classmethod
    def pre_action(cls):
        signal.signal(signal.SIGCHLD, grim_reaper)
