#!/bin/env python
import sys
import os.path
import subprocess


def launch_voila_subprocess(notebook_path, port=8866):
    p = subprocess.Popen([sys.executable, '-m', 'dashboard.voila', notebook_path, str(port)])
    return p


def launch_voila(notebook_path, port=8866):
    print('serving {path}'.format(path=notebook_path))
    from voila.app import Voila
    v = Voila()
    v.notebook_path = notebook_path
    v.port = int(port)
    v.extra_tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors 'self' localhost:*"}}
    v.nbconvert_template_paths.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'voila', 'dashboard', 'nbconvert_templates')))
    v.template_paths.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'voila',  'dashboard', 'templates')))
    v.template = 'dashboard'
    v.start()


if __name__ == '__main__':
    path = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 8866
    launch_voila(path, port)
