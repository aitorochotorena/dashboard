import os
import os.path
import tornado.gen
from tornado.concurrent import run_on_executor
from .handler import HTTPHandler
from .storage import NotebookSQL
from .voila import launch_voila_subprocess
from .utils import find_free_port

ap = os.path.abspath
join = os.path.join


class LaunchHandler(HTTPHandler):
    def initialize(self, dashboard=None, **kwargs):
        self.dashboard = dashboard
        super(LaunchHandler, self).initialize(**kwargs)

    @run_on_executor
    def launch(self, val, id, name):
        if not val:
            self.write({})
            return

        if id in self.dashboard.subprocesses:
            p, nbdir, nbpath, port = self.dashboard.subprocesses[id]

        else:
            nbdir = ap(join(self.dashboard.rundir, id))
            if not os.path.exists(nbdir):
                os.mkdir(nbdir)

            nbpath = ap(join(nbdir, name + '.ipynb'))
            with open(nbpath, 'w') as fp:
                fp.write(val.notebook)

            port = find_free_port()
            p = launch_voila_subprocess(nbpath, port, '/voila/{id}/'.format(id=id), '/',)
            self.dashboard.subprocesses[id] = (p, nbdir, nbpath, port)
        return

    @tornado.gen.coroutine
    def get(self, *args):
        '''Get the login page'''
        val = self.get_argument('val')
        if not val:
            self.write({})
            return

        id, name = val.split('-')
        id = id.strip()
        name = name.strip()

        with self.dashboard.session() as session:
            val = session.query(NotebookSQL).get(int(id))
            _ = yield self.launch(val, id, name)

            ret = val.to_dict()
            p, nbdir, nbpath, port = self.dashboard.subprocesses[id]
            ret['port'] = port
            ret['id'] = id
            ret.pop('notebook', None)  # remove notebook
            self.write(ret)
