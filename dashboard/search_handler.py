import tornado.gen
from tornado.concurrent import run_on_executor
from .handler import HTTPHandler
from .storage import NotebookSQL


class SearchHandler(HTTPHandler):
    def initialize(self, dashboard=None, **kwargs):
        self.dashboard = dashboard
        super(SearchHandler, self).initialize(**kwargs)

    @run_on_executor
    def get_data(self, arg):
        with self.dashboard.session() as session:
            vals = [n.to_dict() for n in session.query(NotebookSQL).filter(NotebookSQL.name.like('%' + arg + '%')).limit(10)]
        return vals

    @tornado.gen.coroutine
    def get(self, *args):
        '''Get the login page'''
        vals = yield self.get_data(self.get_argument('val', ''))
        self.write({'values': vals})
