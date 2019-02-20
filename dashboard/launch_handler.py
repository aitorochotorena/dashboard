import os
import os.path
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

    def get(self, *args):
        '''Get the login page'''
        val = self.get_argument('val')
        if not val:
            self.write({})
            return

        id, name = val.split('-')
        id = id.strip()
        name = name.strip()
        print(id)
        print(name)

        with self.dashboard.session() as session:
            val = session.query(NotebookSQL).get(int(id))
            if not val:
                self.write({})
                return

            if (id, name) in self.dashboard.subprocesses:
                p, nbdir, nbpath, port = self.dashboard.subprocesses[(id, name)]

            else:
                nbdir = ap(join(self.dashboard.rundir, id))
                if not os.path.exists(nbdir):
                    os.mkdir(nbdir)

                nbpath = ap(join(nbdir, name + '.ipynb'))
                with open(nbpath, 'w') as fp:
                    fp.write(val.notebook)

                port = find_free_port()
                p = launch_voila_subprocess(nbpath, port)
                self.dashboard.subprocesses[(id, name)] = (p, nbdir, nbpath, port)

            ret = val.to_dict()
            ret['port'] = port
            self.write(ret)
