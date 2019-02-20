from .handler import HTTPHandler
from .storage import NotebookSQL


class SearchHandler(HTTPHandler):
    def initialize(self, dashboard=None, **kwargs):
        self.dashboard = dashboard
        super(SearchHandler, self).initialize(**kwargs)

    def get(self, *args):
        '''Get the login page'''
        with self.dashboard.session() as session:
            vals = [n.to_dict() for n in session.query(NotebookSQL).filter(NotebookSQL.name.like('%' + self.get_argument('val', '') + '%')).limit(10)]
        self.write({'values': vals})
