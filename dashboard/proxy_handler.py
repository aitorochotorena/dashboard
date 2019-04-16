import os
import os.path
import tornado.web
import tornado.websocket
import tornado.httpclient
from .handler import HTTPHandler

ap = os.path.abspath
join = os.path.join


class ProxyHandler(HTTPHandler):
    def initialize(self, dashboard=None, proxy_path='', **kwargs):
        self.dashboard = dashboard
        self.proxy_path = proxy_path
        super(ProxyHandler, self).initialize(**kwargs)

    @tornado.web.asynchronous
    def get(self, *args):
        '''Get the login page'''
        path = self.request.uri.replace(self.proxy_path, '', 1)
        splits = path.split('/')
        id = splits[0]

        if id not in self.dashboard.subprocesses:
            # self.redirect('/api/v1/launch?val={id}-'.format(id=id))
            return

        p, nbdir, nbpath, port = self.dashboard.subprocesses[id]

        def callback(response):
            if response.body:
                self.write(response.body)
            self.finish()

        req = tornado.httpclient.HTTPRequest('http://localhost:{port}/{url}'.format(port=port, url='/'.join(splits[1:])))
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch(req, callback, raise_error=False)


class ProxyWSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, dashboard=None, proxy_path='', **kwargs):
        super(ProxyWSHandler, self).initialize(**kwargs)
        self.dashboard = dashboard
        self.proxy_path = proxy_path
        self.ws = None

    @tornado.gen.coroutine
    def open(self, *args):
        path = self.request.uri.replace(self.proxy_path, '', 1)
        splits = path.split('/')
        id = splits[0]
        if id not in self.dashboard.subprocesses:
            print('here')
            # self.redirect('/api/v1/launch?val={id}-'.format(id=id))
            return

        p, nbdir, nbpath, port = self.dashboard.subprocesses[id]
        url = '/'.join(splits[1:])

        def write(msg):
            self.ws.write_message(msg)
            print(msg)
        self.ws = yield tornado.websocket.websocket_connect('ws://localhost:{port}/{url}'.format(port=port, url=url),
                                                            on_message_callback=write)

    def on_message(self, message):
        if self.ws:
            self.ws.write_message(message)
        else:
            print('here1')

    def on_close(self):
        if self.ws:
            self.ws.close()
        else:
            print('here2')
