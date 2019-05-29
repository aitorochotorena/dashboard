import os
import os.path
import tornado
import tornado.gen
import tornado.web
import tornado.websocket
import tornado.httpclient
from tornado_proxy_handlers import ProxyHandler, ProxyWSHandler

ap = os.path.abspath
join = os.path.join


class ProxyHandler(ProxyHandler):

    def initialize(self, dashboard=None, proxy_path='', **kwargs):
        self.dashboard = dashboard
        super(ProxyHandler, self).initialize(proxy_path=proxy_path, **kwargs)

    @tornado.gen.coroutine
    def get(self, *args):
        '''Get the login page'''
        path = self.request.uri.replace(self.proxy_path, '', 1)
        splits = path.split('/')
        id = splits[0]

        if id not in self.dashboard.subprocesses:
            return

        p, nbdir, nbpath, port = self.dashboard.subprocesses[id]
        yield super(ProxyHandler, self).get(url='http://localhost:{port}/{url}'.format(port=port, url='/'.join(splits[1:])))


class ProxyWSHandler(ProxyWSHandler):
    def initialize(self, dashboard=None, proxy_path='', **kwargs):
        self.dashboard = dashboard
        super(ProxyWSHandler, self).initialize(proxy_path=proxy_path, **kwargs)

    @tornado.gen.coroutine
    def open(self, *args):
        path = self.request.uri.replace(self.proxy_path, '', 1)
        splits = path.split('/')
        id = splits[0]
        if id not in self.dashboard.subprocesses:
            return

        p, nbdir, nbpath, port = self.dashboard.subprocesses[id]
        url = '/'.join(splits[1:])
        self.closed = False
        yield super(ProxyWSHandler, self).open(url='ws://localhost:{port}/{url}'.format(port=port, url=url))
