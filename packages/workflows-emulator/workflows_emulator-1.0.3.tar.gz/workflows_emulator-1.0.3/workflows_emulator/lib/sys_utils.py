"""
Methods in this module mimic the original ones described in the docs,
but might not be 100% accurate. Some errors might not rise or some hidden
behavior might not be implemented.
"""
from json import dumps as json_dumps
import os
import time
from datetime import datetime

import logging


def get_env(*args):
    return os.getenv(*args)


def log(
    text=None,
    severity: str = 'INFO',
    json=None,
    data=None,
    timeout=None
) -> None:
    log_content = None
    if text is not None:
        log_content = str(text)
    elif json is not None:
        log_content = json_dumps(json, indent=2)
    elif data is not None:
        log_content = json_dumps(data, indent=2)
    if timeout is not None:
        # Timeout is here because the actual runtime makes requests to te GC
        # logging API. We don't need to do that.
        pass
    # if more than one argument is passed, raise an error
    if sum(map(bool, [text, json, data])) > 1:
        raise ValueError(
            'Only one of `[text, json, data]` argument is allowed'
        )
    log_level = logging.getLevelName(severity)
    logger = logging.getLogger("workflows")
    logger.log(log_level, log_content)


def now():
    return time.time()


def sleep(args: dict):
    time.sleep(args['seconds'])


DATE_FORMAT_ISO_8601 = "%Y-%m-%dT%H:%M:%S.%fZ"


def sleep_until(future: str):
    ts_future = datetime.strptime(future, DATE_FORMAT_ISO_8601)
    ts_now = datetime.now()
    delta = ts_future - ts_now
    time.sleep(delta.total_seconds())
