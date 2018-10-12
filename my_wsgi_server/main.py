import sys
from importlib import import_module

import config
from utils import import_spec_object
from process_server import WSGIServerByProcess
from coroutine_server import WSGIServerByCoroutine

SERVER_ADDRESS = (config.SERVER_HOST, config.SERVER_PORT)


def make_server(server_address, application):
    WSGIServer = import_spec_object(config.SERVER)
    WSGIServer.pre_action()
    server = WSGIServer(server_address)
    server.set_app(application)
    return server


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = import_module(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(
        f'WSGIServer: Serving HTTP on port {config.SERVER_HOST}:{config.SERVER_PORT}\n'  # noqa
    )
    httpd.serve_forever()
