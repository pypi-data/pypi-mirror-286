import os, sys
from glob import glob, iglob

import math, cmath
import random

import re
from re import search, sub

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from random import shuffle
from time import sleep, time, monotonic
from functools import partial, reduce, cache
from itertools import tee, count, cycle, repeat, chain, pairwise
from statistics import mean, median, stdev
from pprint import pp
from collections import deque, defaultdict, namedtuple
import logging as log
import subprocess as sp
import threading as thread
import multiprocessing as multi

import json
import pickle

def file_datum(t=None, accuracy=False):
    """
    Usable file datum. T takes a datetime object. Accuracy boolean adds microseconds after a dot.

    :param t: datetime
    :param accuracy: bool
    :return: str
    """
    if t is None:
        t = datetime.now()
    datum = t.strftime("%Y%m%d_%H%M%S"+(".%f" if accuracy else ''))
    return datum

def from_datum(s):
    """
    Reverse of the file datum. Tries several formats and detects accuracy.

    :param s: file datum
    :return: datetime object
    """
    accuracy = bool(search('\.\d+$', s))
    options = [
        "%Y%m%d_%H%M%S" + (".%f" if accuracy else ''),
        "%Y%m%d %H%M%S" + (".%f" if accuracy else ''),
        "%Y/%m/%d %H/%M/%S" + (".%f" if accuracy else ''),
        "%Y/%m/%d %H/%M" + (".%f" if accuracy else '')]
    for x in options:
        try:
            obj = datetime.strptime(s, "%Y%m%d_%H%M%S"+(".%f" if accuracy else ''))
            return obj
        except Exception as ex:
            print(repr(ex))



def force_mkdir(path, critical=False):
    chain = []
    for x in path.split(os.sep):
        chain.append(x)
        _force_mkdir_one(os.sep.join(chain), critical)


def _force_mkdir_one(path, critical=False):
    """
    Catches the file exists error when trying to create a directory. Critical raises FileExistsError if the target is
    actually something else.

    :param path:
    :param critical: bool
    :raises FileExistError
    :return:
    """
    if os.path.exists(path) and not os.path.isdir(path):
        if critical:
            raise FileExistsError(f"{path} is not a directory when trying to create it.")
        else:
            log.debug(f"{path} is not a directory.")
            return
    if os.path.exists(path):
        return

    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def hostname():
    """
    System hostname via sockets

    :return: str
    """
    import socket
    return socket.gethostname()


import traceback
from collections import OrderedDict

class StupidEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return super().default(o)
        except TypeError:
            return repr(o)

def log_trace(stderr=False):
    try:
        force_mkdir('stacktrace')

        for p in glob('stacktrace/*'):
            Δ = datetime.now() - datetime.fromtimestamp(os.stat(p).st_mtime)
            if Δ.total_seconds()/3600/24 > 2:
                try:
                    os.unlink(p)
                except Exception:
                    # At least we tried
                    pass

        p = f'stacktrace{os.sep}{file_datum()}_{os.getpid()}'

        with open(f'{p}.trace','w',encoding='utf8') as f:
            for i, line in enumerate(traceback.format_stack()):
                if stderr and 4 < i < 20:
                    try:
                        l = line
                        if 'b' in sys.stderr.mode:
                            l = l.encode('utf8')
                        sys.stderr.write(l)
                    except UnicodeError:
                        pass

                f.write(line)
            if stderr:
                sys.stderr.flush()

        huge = traceback.StackSummary.extract(traceback.walk_stack(None), capture_locals=True)
        d = OrderedDict()
        for i, l in enumerate(huge):
            try:
                rpr = f"{os.path.basename(l.filename)} #{l.lineno}"
                while rpr in d:
                    rpr+=" \,,/ "
                d[rpr] = {}
                d[rpr]['line'] = l.line
                d[rpr]['lineno'] = l.lineno

                def kill_it(l):
                    if len(l) > 128:
                        return l[0:128]+' <<< over 128 characters >>>'
                    return l

                d[rpr]['locals'] = {k: kill_it(v) for k,v in l.locals.items()}
                if stderr and i<5:
                    json.dump(d[rpr], sys.stderr, cls=StupidEncoder, indent=4)

            except Exception:
                log.debug("Something came up.")
                pass

        with open(p+'_locals.json','w',encoding='utf8') as f:
            json.dump(d, f, cls=StupidEncoder, indent=4)

    except Exception as ex:
        log.error(f"Log trace failed {repr(ex)}")


def sigint_handler(*whatevah):
    if os.path.exists('debug'):
        log_trace(True)
        log.getLogger().setLevel(log.DEBUG)
        log_trace.count = 0
        breakpoint()

        return

    log_trace()

    log_trace.count -= 1
    if log_trace.count <= 0:
        del log_trace.count
        raise KeyboardInterrupt("Count reached")

def install_log_trace():
    import signal
    log_trace.count = 5
    signal.signal(signal.SIGINT, sigint_handler)
