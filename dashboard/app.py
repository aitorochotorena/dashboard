import os
import logging

import tornado.ioloop
import tornado.web

from traitlets.config.application import Application
from traitlets import Unicode, Integer, Bool, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from jupyter_server.utils import url_path_join
from .storage import Base
from .handler import HTMLHandler
from .search_handler import SearchHandler
from .launch_handler import LaunchHandler
from ._version import __version__


class Dashboard(Application):
    name = 'dashboard'
    version = __version__
    description = Unicode('''dashboard''')

    port = Integer(
        8080,
        config=True,
        help='Port of the dashboard server. Default 8867.'
    )

    autoreload = Bool(
        False,
        config=True,
        help='Will autoreload to server and the page when a template, js file or Python code changes'
    )

    baseurl = Unicode(
        '/',
        config=True,
        help='Base URL for running behind reverse proxy'
    )

    sqlalchemy = Unicode(
        'sqlite:///tmp.db',
        config=True,
        help='SQL Alchemy connection string for notebook storage'
    )

    preload_hook = Any(
        help='Preload routine to populate sqlalchemy db from other source'
    )

    upload_hook = Any(
        help='Post-upload routing'
    )

    upload_enable = Bool(
        False,
        config=True,
        help='Enable uploading of notebooks'
    )

    aliases = {
        'port': 'Dashboard.port',
        'autoreload': 'Dashboard.autoreload',
        'sqlalchemy': 'Dashboard.sqlalchemy',
        'upload': 'Dashboard.upload_enable',
        'baseurl': 'Dashboard.baseurl',
    }

    def _init_sqlalchemy(self, sqlalchemy_conn_string):
        self.log.info('Connecting to %s' % self.sqlalchemy)
        self.storage_engine = create_engine(self.sqlalchemy, echo=False)
        Base.metadata.create_all(self.storage_engine)
        self.storage_sessionmaker = sessionmaker(bind=self.storage_engine)

    @contextmanager
    def session(self):
        """Provide a transactional scope around a series of operations."""
        session = self.storage_sessionmaker()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def parse_command_line(self, argv=None):
        super(Dashboard, self).parse_command_line(argv)

    def start(self):
        self.log_level = logging.DEBUG
        root = os.path.join(os.path.dirname(__file__), 'assets')
        static = os.path.join(root, 'static')

        self.app = tornado.web.Application(
            base_url=self.baseurl,
            autoreload=self.autoreload,
            template_path=os.path.join(root, 'templates')
        )

        handlers = [
            (r"/", HTMLHandler, {'template': 'index.html', 'baseurl': self.baseurl}),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static}),
            (url_path_join(self.baseurl, r'/api/v1/search'), SearchHandler, {'dashboard': self}),
            (url_path_join(self.baseurl, r'/api/v1/launch'), LaunchHandler, {'dashboard': self}),
            (r"/(.*)", HTMLHandler, {'template': '404.html'})
        ]

        self.app.add_handlers('.*$', handlers)
        self._init_sqlalchemy(self.sqlalchemy)

        # call initialization routing
        if callable(self.preload_hook):
            self.preload_hook(self.sqlalchemy, self)
        self.listen()

    def listen(self):
        self.app.listen(self.port)
        self.log.info('Dashboard listening on port %s.' % self.port)

        try:
            tornado.ioloop.IOLoop.current().start()
        finally:
            pass


main = Dashboard.launch_instance
