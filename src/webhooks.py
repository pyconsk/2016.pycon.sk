#!/usr/bin/env python
import os

SERVER = os.environ.get('BOTTLE_SERVER', 'wsgiref')

if SERVER == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import sys
import time
import hmac
import hashlib
import logging
from functools import wraps
from subprocess import Popen, PIPE
from bottle import HTTPResponse, request, route, run, json_dumps

SECRET = os.environ.get('BOTTLE_GITHUB_SECRET', '').encode('utf-8')
UPDATE_CMD = '/usr/local/bin/git-update.sh'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(name)s: %(message)s')
logger = logging.getLogger(__name__)


def execute(cmd_id, cmd, stdin=None):
    logger.info('[%s] Running %s', cmd_id, ' '.join(cmd))
    start = time.time()
    exc = Popen(cmd, stdin=PIPE, close_fds=True)
    exc.communicate(input=stdin)
    rc = exc.returncode
    duration = time.time() - start

    if rc == 0:
        logger.info('[%s] Command finished OK in %s seconds', cmd_id, duration)
        return True
    else:
        logger.warn('[%s] Command finished with non-zero exit code (%s) in %s seconds', cmd_id, rc, duration)
        return False


def _verify_signature(payload, signature, secret):
    """Verify GitHub signature"""
    mac = hmac.new(secret, msg=payload, digestmod=hashlib.sha1)

    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)


def verify_signature(secret):
    """verify X-Hub-Signature decorator"""
    def verify_signature_decorator(fun):
        @wraps(fun)
        def wrap(*args, **kwargs):
            if not secret or _verify_signature(request.body.read(), request.headers.get('X-Hub-Signature', ''), secret):
                return fun(*args, **kwargs)
            else:
                return HTTPResponse('invalid signature', status=403)

        return wrap
    return verify_signature_decorator


@route('/webhooks/push', method=('POST',))
@verify_signature(SECRET)
def push():
    data = request.json
    branch = data.get('ref').split('/')[-1]

    try:
        head_commit = data['head_commit']['id']
        cmd_id = head_commit[:8]
    except (TypeError, KeyError):
        head_commit = ''
        cmd_id = str(time.time())

    if execute(cmd_id, [UPDATE_CMD, branch, head_commit], stdin=json_dumps(data).encode('utf-8')):
        return 'ok'
    else:
        return '!!'


run(host=os.environ.get('BOTTLE_HOST', 'localhost'), port=os.environ.get('BOTTLE_PORT', 8080), server=SERVER)
