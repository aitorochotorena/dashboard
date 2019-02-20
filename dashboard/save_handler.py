from .handler import HTTPHandler


class SaveHandler(HTTPHandler):
    def initialize(self, dashboard=None, **kwargs):
        self.dashboard = dashboard
        super(SaveHandler, self).initialize(**kwargs)

    def get(self, *args):
        '''Get the login page'''
        self.write({'values': []})
