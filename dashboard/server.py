import sys
import os.path
import tornado.ioloop
import tornado.web

from .utils import log, parse_args
from .handler import HTMLHandler


def getContext(cache_type='none'):
    d = {}
    return d


class ServerApplication(tornado.web.Application):
    def __init__(self, context, cookie_secret=None, debug=True):
        root = os.path.join(os.path.dirname(__file__), 'assets')
        static = os.path.join(root, 'static')

        default_handlers = [
            (r"/", HTMLHandler, {'template': 'index.html'}),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static}),
            (r"/(.*)", HTMLHandler, {'template': '404.html'})
        ]

        settings = {
                "cookie_secret": cookie_secret or "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                "login_url": "/login",
                "debug": debug,
                "template_path": os.path.join(root, 'templates'),
                }

        super(ServerApplication, self).__init__(default_handlers, **settings)


def main(*args, **kwargs):
    port = kwargs.get('port', 8080)

    context = getContext()

    application = ServerApplication(context)
    log.critical('LISTENING: %s', port)
    application.listen(port)

    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        log.critical('Exiting...')


if __name__ == "__main__":
    args, kwargs = parse_args(sys.argv)
    main(*args, **kwargs)
