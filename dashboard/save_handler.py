from datetime import datetime
from .handler import HTTPHandler
from .storage import NotebookSQL


class SaveHandler(HTTPHandler):
    def initialize(self, dashboard=None, **kwargs):
        self.dashboard = dashboard
        super(SaveHandler, self).initialize(**kwargs)

    def get(self, *args):
        '''Get the login page'''
        created = datetime.now()
        modified = datetime.now()

        with self.dashboard.session() as session:
            vals = [n.name for n in session.query(NotebookSQL).all()]
        self.write({'values': vals})
