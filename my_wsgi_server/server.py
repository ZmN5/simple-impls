class WSGIServer(object):
    def __init__(self, server_address):
        pass

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        pass

    @classmethod
    def pre_action(cls):
        pass
