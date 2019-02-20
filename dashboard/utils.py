try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

import requests
import tornado
import ujson
import logging as log


def parse_body(req, **fields):
    try:
        data = tornado.escape.json_decode(req.body)
    except ValueError:
        data = {}
    return data


def safe_get(path, *args, **kwargs):
    try:
        log.debug('GET: %s' % path)
        resp = requests.get(path, *args, **kwargs).text
        # log.debug('GET_RESPONSE: %s' % resp)
        return ujson.loads(resp)
    except ConnectionRefusedError:
        return {}


def safe_post(path, *args, **kwargs):
    try:
        log.debug('POST: %s' % path)
        resp = requests.post(path, *args, **kwargs).text
        # log.debug('POST_RESPONSE: %s' % resp)
        return ujson.loads(resp)
    except ConnectionRefusedError:
        return {}


def safe_post_cookies(path, *args, **kwargs):
    try:
        log.debug('POST: %s' % path)
        resp = requests.post(path, *args, **kwargs)
        # log.debug('POST_RESPONSE: %s' % resp.text)
        return ujson.loads(resp.text), resp.cookies
    except ConnectionRefusedError:
        return {}, None


def construct_path(host, method):
    return urljoin(host, method)
