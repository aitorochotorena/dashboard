from .handler import HTTPHandler


class LaunchHandler(HTTPHandler):
    def initialize(self, dashboard=None, **kwargs):
        self.dashboard = dashboard
        super(LaunchHandler, self).initialize(**kwargs)

    def get(self, *args):
        '''Get the login page'''
        self.write({'values': ['A sample', 'test list', 'of notebooks']})
