import sys
from datetime import datetime
from io import BytesIO

import config


class AppParams:
    def __init__(self, data):
        self.data = data

    def parse_request(self):
        request_line = self.data.splitlines()[0]
        request_line = request_line.rstrip(b'\r\n')
        (
            self.request_method,
            self.path,
            self.request_version,
        ) = request_line.split()

    def get_environ(self):
        env = {}
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = config.URL_SCHEME
        env['wsgi.input'] = BytesIO(self.data)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        env['REQUEST_METHOD'] = self.request_method
        env['PATH_INFO'] = self.path
        env['SERVER_NAME'] = config.SERVER_NAME
        env['SERVER_PORT'] = str(config.SERVER_PORT)
        return env

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ('Server', config.SERVER_NAME),
        ]
        self.headers_set = [status, response_headers + server_headers]
