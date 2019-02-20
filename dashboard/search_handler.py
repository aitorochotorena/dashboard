from .handler import HTTPHandler
from .storage import NotebookSQL


class SearchHandler(HTTPHandler):
    def initialize(self, dashboard=None, **kwargs):
        self.dashboard = dashboard
        super(SearchHandler, self).initialize(**kwargs)

    def get(self, *args):
        '''Get the login page'''
        with self.dashboard.session() as session:
            vals = [n.name for n in session.query(NotebookSQL).all()]
        self.write({'values': vals})
