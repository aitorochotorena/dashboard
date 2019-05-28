#!/bin/env python
import sys
import subprocess


def launch_voila_subprocess(notebook_path, port=8866, base_url='/', server_url='/'):
    p = subprocess.Popen([sys.executable,
                          '-m',
                          'dashboard.voila',
                          notebook_path,
                          str(port),
                          base_url,
                          server_url
                          ])
    return p


def launch_voila(notebook_path, port=8866, base_url='/', server_url='/'):
    print('serving {path}'.format(path=notebook_path))
    from voila.app import Voila
    v = Voila()
    v.initialize([notebook_path,
                  '--port', port,
                  '--base_url', base_url,
                  '--server_url', server_url,
                  '--no-browser'])
    v.base_url = base_url
    v.server_url = server_url
    v.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors 'self' localhost:*"}}
    v.start()


if __name__ == '__main__':
    path = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 8866
    base_url = sys.argv[3] if len(sys.argv) > 3 else '/'
    server_url = sys.argv[4] if len(sys.argv) > 4 else '/'
    launch_voila(path, port, base_url, server_url)
