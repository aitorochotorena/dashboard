import os
import jinja2

import tornado.ioloop
import tornado.web

from traitlets.config.application import Application
from traitlets import Unicode, Integer, Bool

from jupyter_server.utils import url_path_join
from ._version import __version__


class Dashboard(Application):
    name = 'dashboard'
    version = __version__
    description = Unicode('''dashboard''')

    port = Integer(
        8866,
        config=True,
        help='Port of the dashboard server. Default 8867.'
    )
    autoreload = Bool(
        False,
        config=True,
        help='Will autoreload to server and the page when a template, js file or Python code changes'
    )
    aliases = {
        'port': 'Dashboard.port',
        'autoreload': 'Dashboard.autoreload',
    }

    def parse_command_line(self, argv=None):
        super(Dashboard, self).parse_command_line(argv)

    def start(self):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_paths), extensions=['jinja2.ext.i18n'])
        self.app = tornado.web.Application(
            autoreload=self.autoreload,
            jinja2_env=env,
            static_path='/',
            server_root_dir='/'
        )

        base_url = self.app.settings.get('base_url', '/')

        handlers = [
            (url_path_join(base_url, r'/static/(.*)'),
             tornado.web.StaticFileHandler, {
              'path': os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'static')),
              'default_filename': 'index.html'
             })
        ]

        self.app.add_handlers('.*$', handlers)
        self.listen()

    def listen(self):
        self.app.listen(self.port)
        self.log.info('Dashboard listening on port %s.' % self.port)

        try:
            tornado.ioloop.IOLoop.current().start()
        finally:
            pass


main = Dashboard.launch_instance
